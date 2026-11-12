import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import LaserScan
import math

class ReactiveController(Node):
    def __init__(self):
        super().__init__('reactive_controller')
        
        # Publicador de velocidad (Jazzy requiere TwistStamped)
        self.publisher_ = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        
        # Suscriptor al LIDAR para cerrar el lazo
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        self.get_logger().info("Controlador reactivo iniciado. Explorando y evadiendo...")

    def scan_callback(self, msg):
        # El LIDAR de TurtleBot3 tiene 360 grados.
        # Analizamos un cono frontal de 60 grados (-30 a +30)
        front_ranges = msg.ranges[-30:] + msg.ranges[:30]
        
        # Filtrar valores infinitos o nulos
        valid_ranges = [r for r in front_ranges if not math.isinf(r) and not math.isnan(r)]
        
        if len(valid_ranges) > 0:
            min_distance = min(valid_ranges)
        else:
            min_distance = 10.0  # Asumir que está libre si no hay lecturas

        # Crear el mensaje de movimiento
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = 'base_link'
        
        # Lógica de evasión
        if min_distance < 0.5:
            # Obstáculo cerca: detener y girar sobre su propio eje
            cmd.twist.linear.x = 0.0
            cmd.twist.angular.z = 0.4
        else:
            # Camino libre: avanzar derecho
            cmd.twist.linear.x = 0.15
            cmd.twist.angular.z = 0.0
            
        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = ReactiveController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()