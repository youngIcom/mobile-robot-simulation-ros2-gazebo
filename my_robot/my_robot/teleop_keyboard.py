#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty

# Pesan panduan di terminal
msg = """
===============================
  KONTROL ROBOT DARI KEYBOARD
===============================
Gunakan tombol berikut:
        W
   A    S    D

W/S : Maju / Mundur
A/D : Putar Kiri / Kanan
Spasi : Berhenti total
Q   : Keluar program

Tekan tombol untuk mulai menggerakkan robot!
"""

# Pemetaan tombol ke (arah_maju, arah_putar)
move_bindings = {
    'w': (1.0, 0.0),
    's': (-1.0, 0.0),
    'a': (0.0, 1.0),
    'd': (0.0, -1.0),
    ' ': (0.0, 0.0), # Spasi
}

def get_key(settings):
    # Fungsi ini untuk membaca 1 karakter dari keyboard tanpa harus menekan Enter
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class TeleopKeyboard(Node):
    def __init__(self):
        super().__init__('teleop_keyboard')
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Kecepatan default
        self.speed = 0.5   # m/s
        self.turn = 1.0    # rad/s

    def publish_twist(self, linear, angular):
        twist = Twist()
        twist.linear.x = float(linear * self.speed)
        twist.angular.z = float(angular * self.turn)
        self.cmd_pub.publish(twist)

def main(args=None):
    # Simpan pengaturan awal terminal agar tidak rusak setelah keluar
    settings = termios.tcgetattr(sys.stdin)

    rclpy.init(args=args)
    node = TeleopKeyboard()

    print(msg)

    try:
        while True:
            key = get_key(settings)
            
            # Jika tombol dikenali (w,a,s,d,spasi)
            if key.lower() in move_bindings.keys():
                x = move_bindings[key.lower()][0]
                th = move_bindings[key.lower()][1]
                node.publish_twist(x, th)
                
            # Jika user menekan 'q' atau CTRL+C (\x03)
            elif key.lower() == 'q' or key == '\x03': 
                break
                
    except Exception as e:
        print(f"Terjadi error: {e}")
    finally:
        # Pastikan robot berhenti sebelum program benar-benar keluar
        node.publish_twist(0.0, 0.0)
        
        # Kembalikan terminal ke kondisi semula
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
