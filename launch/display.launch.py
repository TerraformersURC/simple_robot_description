import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node

# this is the function launch  system will look for
def generate_launch_description():

    ####### DATA INPUT ##########
    urdf_file = 'rover.urdf'
    #xacro_file = "urdfbot.xacro"
    package_description = "simple_robot_description"

    ####### DATA INPUT END ##########
    print("Fetching URDF ==>")

    pkg_share = get_package_share_directory(package_description)
    robot_desc_path = os.path.join(pkg_share, "urdf", urdf_file)

    # Robot State Publisher

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher_node',
        emulate_tty=True,

        parameters=[{
        'use_sim_time': True, 
        'robot_description': open(robot_desc_path).read()
        }],

        output="screen"
    )

    # Joint State Publisher

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher_node'
    )

    # RViz Node
    rviz_config_file = os.path.join(pkg_share, 'rviz', 'urdf.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    # create and return launch description object
    return LaunchDescription(
        [            
            robot_state_publisher_node,
            joint_state_publisher_node,
            rviz_node
        ]
    )