#!/usr/bin/env python

import rospy
import roslaunch

import sys
 
import subprocess
import re

def find_webcam_by_name(device_name):
    # Run v4l2-ctl to list video devices
    result = subprocess.run(['v4l2-ctl', '--list-devices'], capture_output=True, text=True)
    video_devices = result.stdout

    # Use regex to find the device with the specified name
    pattern = re.compile(rf'{re.escape(device_name)}:.*?(/dev/video\d+)', re.DOTALL)
    match = pattern.search(video_devices)

    # Check if the webcam information is found
    if match:
        # Extract the video device path
        video_device_path = match.group(1)
        
        print("Found Webcam Information:")
        print(video_devices)

        print(f"Associated {video_device_path}")
        return video_device_path
    else:
        print(f"Webcam with device name '{device_name}' not found.")


if __name__ == '__main__':
    rospy.init_node('usb_cam_launcher', anonymous=True)

    package = 'launch_usbcam'  # Replace with your ROS package name
    launch_file = 'usbcam.launch'
    device_name_to_find = "USB 2.0 Camera"
    # Find and print information about the webcam
    device_name = find_webcam_by_name(device_name_to_find)
    # Specify the camera device as an argument
    camera_device_arg = rospy.get_param('~camera_device', device_name)

    # Create a launch configuration with the specified argument
    launch_args = [package, launch_file, f'camera_device:={camera_device_arg}']

    # Launch the node
    roslaunch_args = launch_args[1:]
    roslaunch_file = [(roslaunch.rlutil.resolve_launch_arguments(launch_args)[0], roslaunch_args)]
    parent = roslaunch.parent.ROSLaunchParent(rospy.get_param("/run_id"), roslaunch_file)
    
    try:
        parent.start()
        rospy.loginfo("USB Cam node launched successfully.")
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    finally:
        parent.shutdown()
