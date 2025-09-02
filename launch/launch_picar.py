from launch import LaunchDescription
from launch_ros.actions import Node


# ROS Launch file for the Raspberry Pi on the PiCar-X
def generate_launch_description():
    return LaunchDescription([
        # Launch the camera node to get access to the Raspberry Pi Camera
        Node(
            package='camera_ros',
            executable='camera_node',
            name='pix_camera',
            parameters=[{"format": "YUYV", "width": 320, "height": 240}]
        ),
        # Launch the PIX Driver Node to control the car
        Node(
            package='pix_driver',
            executable='pix_node',
            name='pix_control',
            # Mofify Code parameters without recompiling
            parameters=[{"turn_offset": 1.0, "diff_ratio": 0.65}]
            ),
    ])
