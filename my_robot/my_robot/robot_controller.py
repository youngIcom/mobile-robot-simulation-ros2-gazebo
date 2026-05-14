#!/usr/bin/env python3

# --- BAGIAN 1: IMPORT ---
# Mengimpor 'batu bata' bawaan ROS 2. 
import rclpy
from rclpy.node import Node
# Twist adalah tipe data standar untuk kecepatan (maju/mundur/belok)
from geometry_msgs.msg import Twist
# Odometry adalah tipe data standar untuk posisi (x, y, z, dan rotasi)
from nav_msgs.msg import Odometry
import math

# --- BAGIAN 2: MEMBUAT KELAS NODE (SANG OTAK) ---
class RobotController(Node):
    def __init__(self):
        # Memberikan nama resmi pada node ini
        super().__init__('robot_controller')

        # [KENOP PUTAR] Mendeklarasikan Parameter
        # Format: (nama_parameter, nilai_default)
        self.declare_parameter('target_linear_speed', 0.5)
        self.declare_parameter('target_angular_speed', 0.5)
        self.declare_parameter('publish_rate', 10.0)

        # Mengambil nilai rate (berapa kali per detik otak ini berpikir)
        publish_rate = self.get_parameter('publish_rate').value

        # [MULUT] Membuat Publisher
        # "Aku akan berteriak dengan tipe pesan Twist, ke saluran /cmd_vel, dengan kapasitas antrean 10 pesan"
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # [MATA] Membuat Subscriber
        # "Aku akan mendengarkan tipe pesan Odometry, dari saluran /odom, dan setiap kali ada pesan masuk, jalankan fungsi odom_callback"
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        # Variabel memori otak untuk mengingat posisi
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0

        # Detak Jantung Otak: Timer yang akan mengeksekusi fungsi publish_cmd berulang kali
        self.timer = self.create_timer(1.0 / publish_rate, self.publish_cmd)
        
        self.get_logger().info('RobotController menyala! Mulai bergerak.')

    # --- BAGIAN 3: FUNGSI REAKSI (CALLBACK) ---
    def odom_callback(self, msg: Odometry):
        # Merekam posisi X dan Y
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        
        # Matematika kompleks (Quaternion) untuk mengubah rotasi 3D menjadi derajat (Yaw/hadapan)
        q = msg.pose.pose.orientation
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.current_yaw = math.atan2(siny_cosp, cosy_cosp)

    def publish_cmd(self):
        # 1. Baca nilai kenop putar terbaru saat ini
        linear = self.get_parameter('target_linear_speed').value
        angular = self.get_parameter('target_angular_speed').value

        # 2. Siapkan pesannya
        msg = Twist()
        msg.linear.x = linear    # Kecepatan maju lurus
        msg.angular.z = angular  # Kecepatan putar

        # 3. Teriakkan ke motor!
        self.cmd_pub.publish(msg)

# --- BAGIAN 4: TITIK AWAL PROGRAM ---
def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    rclpy.spin(node)  # Tahan program ini agar tidak langsung mati setelah dijalankan
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()