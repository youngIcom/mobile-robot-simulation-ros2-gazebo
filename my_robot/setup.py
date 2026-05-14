from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_robot'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # tambahan
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yesaya',
    maintainer_email='yesayasentosa@gmail.com',
    description='Mobile robot simulation with ROS 2 and Gazebo',
    license='MIT',
    entry_points={
        'console_scripts': [
            'robot_controller = my_robot.robot_controller:main',
            'speed_service = my_robot.speed_service:main',
            'drive_action_server = my_robot.drive_action_server:main',
            'teleop_keyboard = my_robot.teleop_keyboard:main',
        ],
    },
)
