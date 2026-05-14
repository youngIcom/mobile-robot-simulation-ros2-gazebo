#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import time

# Mengimpor kertas pesanan kita!
from my_robot_interfaces.action import DriveDistance

class DriveActionServer(Node):
    def __init__(self):
        super().__init__('drive_action_server')
        
        # Multithreading: Agar robot bisa jalan sekaligus mengirim feedback
        self.cb_group = ReentrantCallbackGroup()

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10, callback_group=self.cb_group)

        self.current_x = 0.0
        self.current_y = 0.0

        # [RESTORAN] Membuat Action Server
        self._action_server = ActionServer(
            self,
            DriveDistance,
            'drive_distance',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=self.cb_group
        )
        self.get_logger().info('Action Server Siap! Menunggu pesanan rute...')

    def odom_callback(self, msg: Odometry):
        # Terus update posisi robot saat ini
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

    def goal_callback(self, goal_request):
        self.get_logger().info(f'Terima pesanan: Jalan {goal_request.distance} meter')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Pesanan DIBATALKAN oleh Penelepon!')
        return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        self.get_logger().info('Mulai mengeksekusi pesanan...')

        target_distance = goal_handle.request.distance
        speed = goal_handle.request.speed
        
        feedback_msg = DriveDistance.Feedback()
        result = DriveDistance.Result()

        # Catat posisi awal
        start_x = self.current_x
        start_y = self.current_y

        # Perintah gerak
        twist = Twist()
        twist.linear.x = speed

        while True:
            # 1. Cek apakah ada permintaan Batal
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.stop_robot()
                result.success = False
                result.total_distance = self.compute_distance(start_x, start_y)
                return result

            # 2. Hitung jarak yang sudah ditempuh (Rumus Pythagoras)
            dist = self.compute_distance(start_x, start_y)

            # 3. Jika sudah sampai tujuan, hentikan loop
            if dist >= target_distance:
                break

            # 4. Jalan dan Kirim Feedback (Live Tracking)
            self.cmd_pub.publish(twist)
            feedback_msg.current_distance = dist
            feedback_msg.percentage = (dist / target_distance) * 100.0
            goal_handle.publish_feedback(feedback_msg)
            
            time.sleep(0.1)

        # Selesai! Rem robot dan kirim Result
        self.stop_robot()
        result.total_distance = self.compute_distance(start_x, start_y)
        result.success = True
        goal_handle.succeed()
        
        self.get_logger().info(f'SUKSES! Sampai di tujuan.')
        return result

    def compute_distance(self, start_x, start_y):
        dx = self.current_x - start_x
        dy = self.current_y - start_y
        return math.sqrt(dx * dx + dy * dy)

    def stop_robot(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.cmd_pub.publish(twist)

from rclpy.executors import MultiThreadedExecutor

def main(args=None):
    rclpy.init(args=args)
    node = DriveActionServer()
    executor = MultiThreadedExecutor()
    rclpy.spin(node, executor=executor)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()