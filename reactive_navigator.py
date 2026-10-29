#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped
import numpy as np

class ReactiveNavigator(Node):
    def __init__(self):
        super().__init__('reactive_navigator')
        
        # Suscriptor LiDAR (/scan)
        self.sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        
        # Publisher TwistStamped (/cmd_vel)
        self.pub = self.create_publisher(
            TwistStamped,
            '/cmd_vel',
            10
        )
        self.get_logger().info('Nodo ReactiveNavigator iniciado. Leyendo /scan...')

    def scan_callback(self, msg):
        ranges = np.array(msg.ranges)
        n = len(ranges)
        if n == 0:
            return

        # Sector frontal del TurtleBot3 (primeros y últimos 30 grados del barrido)
        front_indices = np.concatenate((ranges[:n//12], ranges[-n//12:]))
        
        # Limpiar valores inválidos (inf, nan)
        valid_front = front_indices[np.isfinite(front_indices)]
        if len(valid_front) == 0:
            front = 3.5
        else:
            front = np.min(valid_front)

        cmd = TwistStamped()
        # Header
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = 'base_link'

        # Lógica reactiva
        if front < 0.5:
            cmd.twist.linear.x = 0.0
            cmd.twist.angular.z = 0.8
            accion = "OBSTACULO (<0.5m) -> GIRANDO"
        else:
            cmd.twist.linear.x = 0.2
            cmd.twist.angular.z = 0.0
            accion = "LIBRE -> AVANZANDO"

        self.pub.publish(cmd)
        self.get_logger().info(f'Dist. Frontal: {front:.2f} m | {accion}')

def main(args=None):
    rclpy.init(args=args)
    node = ReactiveNavigator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()