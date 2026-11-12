#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped, Point
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, NavSatFix, LaserScan
from std_msgs.msg import Float32MultiArray
from visualization_msgs.msg import Marker, MarkerArray
from tf2_ros import TransformBroadcaster
import numpy as np
import math

class DroneSTNSimulator(Node):
    def __init__(self):
        super().__init__('drone_stn_simulator')

        # Parámetros de la línea STN 500 kV (Colombia)
        self.declare_parameter('num_towers', 6)         # Escalar a 22 para los 10 km completos
        self.declare_parameter('span_length', 450.0)    # 450 m de vano promedio
        self.declare_parameter('tower_height', 50.0)    # 50 m (rango 40-60 m para 500 kV)
        self.declare_parameter('sag_guard', 6.5)        # Flecha máxima del cable de guarda [m]

        self.num_towers = self.get_parameter('num_towers').value
        self.span = self.get_parameter('span_length').value
        self.h_tower = self.get_parameter('tower_height').value
        self.sag = self.get_parameter('sag_guard').value

        # Estado 6-DoF del cuadricóptero en SE(3): [x, y, z, roll, pitch, yaw]
        self.pos = np.array([0.0, -12.0, 52.0], dtype=float)
        self.vel = np.zeros(3, dtype=float)
        self.rpy = np.zeros(3, dtype=float)
        self.cmd_vel = np.zeros(4, dtype=float) # [vx, vy, vz, wz]

        # Fallas sembradas en la línea [x_m, y_m, z_m, tipo_codigo, severidad_C]
        # Tipo 1: Hebra rota en cable de guarda | Tipo 2: Punto caliente en aislador/fase (145 °C)
        self.faults = [
            np.array([225.0, 0.0, self.h_tower - self.sag, 1.0, 85.0]),
            np.array([450.0, 0.0, self.h_tower, 2.0, 148.5]),
            np.array([1125.0, 0.0, self.h_tower - self.sag, 1.0, 92.0]),
            np.array([1800.0, 0.0, self.h_tower, 2.0, 165.0])
        ]

        # Suscriptor de comandos de vuelo (del controlador autónomo)
        self.sub_cmd = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)

        # Publicadores de Estado y Sensores
        self.pub_odom = self.create_publisher(Odometry, '/odom', 10)
        self.pub_imu = self.create_publisher(Imu, '/imu/data_raw', 10)
        self.pub_gps = self.create_publisher(NavSatFix, '/gps/fix', 10)
        self.pub_lidar = self.create_publisher(LaserScan, '/scan', 10)
        self.pub_payload = self.create_publisher(Float32MultiArray, '/camera_4t/line_telemetry', 10)
        self.pub_markers = self.create_publisher(MarkerArray, '/stn_500kv_environment', 10)

        self.tf_broadcaster = TransformBroadcaster(self)

        self.dt = 0.05 # 20 Hz
        self.timer = self.create_timer(self.dt, self.step_simulation)
        self.timer_env = self.create_timer(2.0, self.publish_stn_environment)

        self.get_logger().info(
            f'Simulador Autel EVO Max 4T iniciado: {self.num_towers} torres de 500 kV '
            f'({self.h_tower} m altura, {self.span} m vano).'
        )

    def cmd_callback(self, msg: Twist):
        self.cmd_vel[0] = msg.linear.x
        self.cmd_vel[1] = msg.linear.y
        self.cmd_vel[2] = msg.linear.z
        self.cmd_vel[3] = msg.angular.z

    def get_guard_wire_z(self, x_pos: float) -> float:
        """Calcula la altura de la catenaria del cable de guarda en la coordenada X."""
        if x_pos < 0.0 or x_pos > (self.num_towers - 1) * self.span:
            return self.h_tower
        x_local = (x_pos % self.span) - (self.span / 2.0)
        return self.h_tower - self.sag * (1.0 - (2.0 * x_local / self.span) ** 2)

    def step_simulation(self):
        now = self.get_clock().now().to_msg()

        # 1. Dinámica de vuelo y actitud acoplada (Corke Cap. 4: inclinación para traslación)
        tau_resp = 0.25
        yaw = self.rpy[2]
        vx_world = self.cmd_vel[0] * math.cos(yaw) - self.cmd_vel[1] * math.sin(yaw)
        vy_world = self.cmd_vel[0] * math.sin(yaw) + self.cmd_vel[1] * math.cos(yaw)
        vz_world = self.cmd_vel[2]

        self.vel += (np.array([vx_world, vy_world, vz_world]) - self.vel) * (self.dt / tau_resp)
        self.pos += self.vel * self.dt
        self.rpy[2] += self.cmd_vel[3] * self.dt

        # Ángulos de pitch y roll inducidos por la aceleración/velocidad traslacional
        self.rpy[1] = np.clip(0.04 * self.cmd_vel[0], -0.35, 0.35)  # Pitch
        self.rpy[0] = np.clip(-0.04 * self.cmd_vel[1], -0.35, 0.35) # Roll

        # 2. Cálculo de distancia al cable de guarda y nivel de Interferencia Electromagnética (EMI)
        z_wire = self.get_guard_wire_z(self.pos[0])
        dist_to_wire = math.sqrt((self.pos[1] - 0.0)**2 + (self.pos[2] - z_wire)**2)
        # Campo magnético B proporcional a 1/r cerca de la línea de 500 kV [microTesla]
        emi_intensity_uT = 180.0 / max(dist_to_wire, 0.5)

        # 3. Publicar TF (world -> base_link) y Odometría limpia (Estimador LiDAR-Inercial)
        q = self.euler_to_quat(self.rpy[0], self.rpy[1], self.rpy[2])
        t = TransformStamped()
        t.header.stamp = now
        t.header.frame_id = 'world'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = float(self.pos[0])
        t.transform.translation.y = float(self.pos[1])
        t.transform.translation.z = float(self.pos[2])
        t.transform.rotation.x, t.transform.rotation.y, t.transform.rotation.z, t.transform.rotation.w = q
        self.tf_broadcaster.sendTransform(t)

        odom = Odometry()
        odom.header = t.header
        odom.child_frame_id = 'base_link'
        odom.pose.pose.position.x = float(self.pos[0])
        odom.pose.pose.position.y = float(self.pos[1])
        odom.pose.pose.position.z = float(self.pos[2])
        odom.pose.pose.orientation = t.transform.rotation
        self.pub_odom.publish(odom)

        # 4. SENSOR AFECTADO POR EMI #1: IMU / Magnetómetro (/imu/data_raw)
        imu_msg = Imu()
        imu_msg.header.stamp = now
        imu_msg.header.frame_id = 'imu_link'
        sigma_mag = 0.02 + 0.015 * emi_intensity_uT # Ruido severo en orientación por 500 kV
        noisy_yaw = self.rpy[2] + np.random.normal(0.0, sigma_mag)
        qi = self.euler_to_quat(self.rpy[0], self.rpy[1], noisy_yaw)
        imu_msg.orientation.x, imu_msg.orientation.y, imu_msg.orientation.z, imu_msg.orientation.w = qi
        imu_msg.orientation_covariance[8] = float(sigma_mag ** 2)
        self.pub_imu.publish(imu_msg)

        # 5. SENSOR AFECTADO POR EMI #2: GPS (/gps/fix)
        gps_msg = NavSatFix()
        gps_msg.header.stamp = now
        gps_msg.header.frame_id = 'base_link'
        sigma_gps = 0.3 + 0.08 * emi_intensity_uT # Saltos de varios metros cerca de la torre
        # Coordenadas base en Caldas/Antioquia (STN Colombia)
        gps_msg.latitude = 5.0689 + (self.pos[1] + np.random.normal(0, sigma_gps)) / 111111.0
        gps_msg.longitude = -75.5174 + (self.pos[0] + np.random.normal(0, sigma_gps)) / 111111.0
        gps_msg.altitude = float(self.pos[2] + np.random.normal(0, sigma_gps * 1.5))
        self.pub_gps.publish(gps_msg)

        # 6. SENSOR INMUNE A EMI #1: LiDAR 3D (/scan) - Precisión milimétrica (sigma = 0.01 m)
        scan = LaserScan()
        scan.header.stamp = now
        scan.header.frame_id = 'lidar_link'
        scan.angle_min = -math.pi / 2
        scan.angle_max = math.pi / 2
        scan.angle_increment = math.pi / 60
        scan.range_min = 0.2
        scan.range_max = 50.0
        clean_dist = float(dist_to_wire + np.random.normal(0.0, 0.008))
        scan.ranges = [clean_dist for _ in range(60)]
        self.pub_lidar.publish(scan)

        # 7. SENSOR INMUNE A EMI #2: Cámara Térmica/Óptica 4T (/camera_4t/line_telemetry)
        # Formato: [x_dron, z_cable_guarda, dist_limpia_lidar, emi_uT, codigo_falla, temp_C]
        fault_code = 0.0
        temp_detected = 28.5 + np.random.normal(0.0, 0.4) # Temperatura normal del cable
        for f in self.faults:
            if np.linalg.norm(self.pos[:2] - f[:2]) < 12.0:
                fault_code = float(f[3])
                temp_detected = float(f[4] + np.random.normal(0.0, 0.5))
                break

        telemetry = Float32MultiArray()
        telemetry.data = [
            float(self.pos[0]), float(z_wire), clean_dist,
            float(emi_intensity_uT), fault_code, float(temp_detected)
        ]
        self.pub_payload.publish(telemetry)

    def publish_stn_environment(self):
        """Publica en RViz2 las torres de 500 kV (50 m), conductores de fase y cable de guarda."""
        ma = MarkerArray()
        now = self.get_clock().now().to_msg()

        # Torres de transmisión de 500 kV cada 450 m
        for i in range(self.num_towers):
            x_t = float(i * self.span)
            m = Marker()
            m.header.frame_id = 'world'
            m.header.stamp = now
            m.ns = 'towers_500kv'
            m.id = i
            m.type = Marker.CYLINDER
            m.action = Marker.ADD
            m.pose.position.x = x_t
            m.pose.position.y = 0.0
            m.pose.position.z = self.h_tower / 2.0
            m.scale.x = 3.5
            m.scale.y = 3.5
            m.scale.z = self.h_tower
            m.color.r, m.color.g, m.color.b, m.color.a = (0.55, 0.58, 0.62, 0.9)
            ma.markers.append(m)

        # Cable de guarda superior (Catenaria a 50 m) y Conductores de Fase (a 40 m)
        guard_line = Marker()
        guard_line.header.frame_id = 'world'
        guard_line.header.stamp = now
        guard_line.ns = 'guard_wire'
        guard_line.id = 100
        guard_line.type = Marker.LINE_STRIP
        guard_line.scale.x = 0.35
        guard_line.color.r, guard_line.color.g, guard_line.color.b, guard_line.color.a = (0.95, 0.85, 0.1, 1.0)

        max_x = (self.num_towers - 1) * self.span
        for x_val in np.linspace(0.0, max_x, 120):
            p = Point()
            p.x = float(x_val)
            p.y = 0.0
            p.z = float(self.get_guard_wire_z(x_val))
            guard_line.points.append(p)
        ma.markers.append(guard_line)

        self.pub_markers.publish(ma)

    @staticmethod
    def euler_to_quat(roll, pitch, yaw):
        cy, sy = math.cos(yaw * 0.5), math.sin(yaw * 0.5)
        cp, sp = math.cos(pitch * 0.5), math.sin(pitch * 0.5)
        cr, sr = math.cos(roll * 0.5), math.sin(roll * 0.5)
        return (
            sr * cp * cy - cr * sp * sy,
            cr * sp * cy + sr * cp * sy,
            cr * cp * sy - sr * sp * cy,
            cr * cp * cy + sr * sp * sy
        )

def main(args=None):
    rclpy.init(args=args)
    node = DroneSTNSimulator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
