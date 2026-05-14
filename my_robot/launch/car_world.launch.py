import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_dir = get_package_share_directory('my_robot')
    
    # Path ke file 'robot.urdf' kamu (yang sebenarnya adalah SDF)
    world_file = os.path.join(pkg_dir, 'urdf', 'robot.urdf')

    # Menjalankan gazebo harmonic langsung dengan memuat file world tersebut
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        # Ganti empty.sdf dengan file world buatanmu
        launch_arguments={'gz_args': f'-r {world_file}'}.items()
    )

    return LaunchDescription([
        gz_sim
    ])
