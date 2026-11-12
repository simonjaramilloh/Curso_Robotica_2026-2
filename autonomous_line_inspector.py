#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32MultiArray
from visualization_msgs.msg import Marker
import numpy as np
import csv
import os
from datetime import datetime

class AutonomousLineInspector(Node):
    def __init__(self):
        super().__init__('autonomous_line_inspector')

        self.declare_parameter('num_towers', 6)
        self.declare_parameter('span_length', 450.0)
        self.declare_parameter('cruise_speed', 15.0) # m/s para cubrir vanos de 450 m ágilmente

        self.num_towers = self.get_parameter('num_towers').value
        self.span = self.get_parameter('span_length').value
        self.v_cruise = self.get_parameter('cruise_speed').value
        self.total_distance = (self.num_towers - 1) * self.span

        self.pos = np.array([0.0, -12.0, 52.0])
        self.yaw = 0.0
        self.telemetry = [0.0, 50.0, 3.0, 0.0, 0.0, 28.0]
        self.detected_positions = []

        # Suscriptores y Publicadores
        self.sub_odom = self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        self.sub_tel = self.create_subscription(
            Float32MultiArray, '/camera_4t/line_telemetry', self.telemetry_cb, 10
        )
        self.pub_cmd = self.create_publisher(Twist, '/cmd_vel', 10)
        self.pub_path_marker = self.create_publisher(Marker, '/drone_inspection_trail', 10)
        self.pub_fault_marker = self.create_publisher(Marker, '/detected_faults_markers', 10)

        # Inicializar archivo CSV para almacenar el recorrido y diagnóstico
        self.csv_path = os.path.expanduser('~/reporte_inspeccion_stn_500kv.csv')
        self.csv_file = open(self.csv_path, mode='w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow([
            'Timestamp', 'X_m', 'Y_m', 'Z_m', 'Vano_Actual',
            'Dist_CableGuarda_m', 'EMI_uT', 'Temp_C', 'Estado_Diagnostico'
        ])

        self.path_marker = Marker()
        self.path_marker.header.frame_id = 'world'
        self.path_marker.ns = 'drone_trail'
        self.path_marker.id = 1
        self.path_marker.type = Marker.LINE_STRIP
        self.path_marker.scale.x = 0.5
        self.path_marker.color.r, self.path_marker.color.g, self.path_marker.color.b, self.path_marker.color.a = (0.0, 1.0, 0.4, 1.0)

        self.fault_marker = Marker()
        self.fault_marker.header.frame_id = 'world'
        self.fault_marker.ns = 'fault_points'
        self.fault_marker.id = 2
        self.fault_marker.type = Marker.SPHERE_LIST
        self.fault_marker.scale.x = 4.0
        self.fault_marker.scale.y = 4.0
        self.fault_marker.scale.z = 4.0
        self.fault_marker.color.r, self.fault_marker.color.g, self.fault_marker.color.b, self.fault_marker.color.a = (1.0, 0.1, 0.1, 1.0)

        self.timer = self.create_timer(0.1, self.control_and_diagnose)
        self.mission_completed = False
        self.get_logger().info(f'Iniciando recorrido autónomo STN 500 kV. Guardando datos en: {self.csv_path}')

    def odom_cb(self, msg: Odometry):
        self.pos[0] = msg.pose.pose.position.x
        self.pos[1] = msg.pose.pose.position.y
        self.pos[2] = msg.pose.pose.position.z
        q = msg.pose.pose.orientation
        self.yaw = np.arctan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y**2 + q.z**2))

    def telemetry_cb(self, msg: Float32MultiArray):
        self.telemetry = msg.data

    def control_and_diagnose(self):
        if self.mission_completed:
            return

        _, z_wire, clean_dist, emi_uT, fault_code, temp_c = self.telemetry
        vano_idx = int(self.pos[0] // self.span) + 1

        # 1. Control en cascada de seguimiento de línea (offset lateral Y = -2.5 m, Z = z_wire + 2.5 m)
        y_ref = -2.5
        z_ref = z_wire + 2.5

        cmd = Twist()
        if self.pos[0] >= self.total_distance:
            cmd.linear.x = 0.0
            cmd.linear.y = 0.0
            cmd.linear.z = 0.0
            self.pub_cmd.publish(cmd)
            self.mission_completed = True
            self.csv_file.close()
            self.get_logger().info(
                f'¡RECORRIDO COMPLETADO ({self.total_distance:.0f} m)! '
                f'Reporte final almacenado en: {self.csv_path}'
            )
            return

        cmd.linear.x = float(self.v_cruise)
        cmd.linear.y = float(np.clip(1.8 * (y_ref - self.pos[1]), -4.0, 4.0))
        cmd.linear.z = float(np.clip(2.0 * (z_ref - self.pos[2]), -4.0, 4.0))
        cmd.angular.z = float(np.clip(-2.0 * self.yaw, -1.0, 1.0))
        self.pub_cmd.publish(cmd)

        # 2. Diagnóstico en directo y almacenamiento
        if fault_code == 1.0:
            estado = 'ALERTA: Rotura de hebra en Cable de Guarda'
            self.register_fault_marker()
            self.get_logger().warn(
                f'[Vano {vano_idx} | X={self.pos[0]:.1f}m] {estado} | Temp={temp_c:.1f}°C | EMI={emi_uT:.1f}uT'
            )
        elif fault_code == 2.0:
            estado = 'CRITICO: Punto Caliente en Aislador/Fase 500kV'
            self.register_fault_marker()
            self.get_logger().error(
                f'[Torre {vano_idx} | X={self.pos[0]:.1f}m] {estado} | Temp={temp_c:.1f}°C | EMI={emi_uT:.1f}uT'
            )
        else:
            estado = 'NOMINAL'
            self.get_logger().info(
                f'[Vano {vano_idx} | X={self.pos[0]:.1f}m/{self.total_distance:.0f}m] '
                f'Guarda OK (d={clean_dist:.2f}m) | Temp={temp_c:.1f}°C | EMI={emi_uT:.1f}uT',
                throttle_duration_sec=1.5
            )

        self.csv_writer.writerow([
            datetime.now().strftime('%H:%M:%S.%f')[:-3],
            f'{self.pos[0]:.2f}', f'{self.pos[1]:.2f}', f'{self.pos[2]:.2f}',
            vano_idx, f'{clean_dist:.3f}', f'{emi_uT:.2f}', f'{temp_c:.1f}', estado
        ])

        # Actualizar estela en RViz2
        now = self.get_clock().now().to_msg()
        self.path_marker.header.stamp = now
        p = Point(x=float(self.pos[0]), y=float(self.pos[1]), z=float(self.pos[2]))
        self.path_marker.points.append(p)
        self.pub_path_marker.publish(self.path_marker)

    def register_fault_marker(self):
        if all(np.linalg.norm(self.pos - fp) > 15.0 for fp in self.detected_positions):
            self.detected_positions.append(self.pos.copy())
            p = Point(x=float(self.pos[0]), y=0.0, z=float(self.pos[2]))
            self.fault_marker.header.stamp = self.get_clock().now().to_msg()
            self.fault_marker.points.append(p)
            self.pub_fault_marker.publish(self.fault_marker)

def main(args=None):
    rclpy.init(args=args)
    node = AutonomousLineInspector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if not node.csv_file.closed:
            node.csv_file.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
