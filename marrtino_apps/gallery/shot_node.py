#!/usr/bin/python
# -*- coding:utf-8 -*-
import rospy 
from std_msgs.msg import String

import sys
import cv2
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


def capture_photo(device_name, output_file):
    # Open the video capture object
    #  4608x2592

    cap = cv2.VideoCapture(device_name)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2592)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Could not read frame.")
        cap.release()
        return

    # Save the captured frame to a file
    cv2.imwrite(output_file, frame)

    # Release the video capture object
    cap.release()

    print(f"Photo captured and saved to {output_file}")



def callback(data):
    rospy.loginfo('I shot %s', data.data)
    try:
        ## Specify the device name of your webcam
        device_name_to_find = "Arducam_12MP"
        photo_filename = "images/" + data.data
        # Find and print information about the webcam
        device_name = find_webcam_by_name(device_name_to_find)
        print("Device Name :",device_name)
        capture_photo(device_name,photo_filename)

    except Exception as e:
        print("receive msg,but parse exception:", e)

   
    
if __name__ == '__main__':
    rospy.init_node('shot_node', anonymous=True)
    rospy.loginfo('Start shot_node')
    rospy.Subscriber('shot', String, callback, queue_size=1)
    rospy.spin()




