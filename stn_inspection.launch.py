from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_dir = get_package_share_directory('autel_stn_inspector')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'autel_evo_max.urdf')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc}]
        ),
        Node(
            package='autel_stn_inspector',
            executable='drone_stn_simulator',
            name='drone_stn_simulator',
            output='screen',
            parameters=[{
                'num_towers': 6,        # Cambiar a 22 para simular los 10 km completos
                'span_length': 450.0,
                'tower_height': 50.0
            }]
        ),
        Node(
            package='autel_stn_inspector',
            executable='autonomous_line_inspector',
            name='autonomous_line_inspector',
            output='screen',
            parameters=[{
                'num_towers': 6,
                'span_length': 450.0,
                'cruise_speed': 20.0
            }]
        )
    ])
