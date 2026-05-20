#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

# Mengimpor bahasa kamus yang baru saja kita buat!
from my_robot_interfaces.srv import SetSpeed

class SpeedServiceNode(Node):
    def __init__(self):
        super().__init__('speed_service_node')

        # Parameter untuk batas keamanan
        self.declare_parameter('max_linear_speed', 0.6)
        self.max_linear = self.get_parameter('max_linear_speed').value

        # Publisher untuk langsung menggerakkan roda (Mulut)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # [TELEPON] Membuat Service Server
        # "Aku membuka saluran bernama 'set_speed'. Jika ada yang menelepon dengan format SetSpeed, arahkan ke fungsi set_speed_callback"
        self.srv = self.create_service(SetSpeed, 'set_speed', self.set_speed_callback)

        self.get_logger().info('SpeedService siap! Menunggu telepon masuk di /set_speed...')

    def set_speed_callback(self, request, response):
        # 1. Menerima data telepon
        self.get_logger().info(f'Menerima permintaan: linear={request.linear_speed}')

        # 2. Mengecek keamanan (Validasi)
        if abs(request.linear_speed) > self.max_linear:
            # Jika terlalu cepat, tolak!
            response.success = False
            response.message = f'Gagal! Kecepatan melebih batas maksimal ({self.max_linear})'
            return response

        # 3. Jika aman, perintahkan roda bergerak
        msg = Twist()
        msg.linear.x = request.linear_speed
        msg.angular.z = request.angular_speed
        self.cmd_pub.publish(msg)

        # 4. Berikan balasan sukses
        response.success = True
        response.message = f'Sukses! Kecepatan diatur ke {request.linear_speed}'
        return response

def main(args=None):
    rclpy.init(args=args)
    node = SpeedServiceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()