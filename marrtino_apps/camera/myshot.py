import cv2
import subprocess
import re

# get resolution
# v4l2-ctl -d /dev/video0 --list-formats-ext

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


# Capture the photo
capture_photo(device_name, output_file)

def main():
    # Check the number of command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python shot.py <nomefile.jpg>")
        sys.exit(1)

    # Access the command-line parameter
    photo_filename = sys.argv[1]

    ## Specify the device name of your webcam
    device_name_to_find = "Arducam_12MP"

    # Find and print information about the webcam
    device_name = find_webcam_by_name(device_name_to_find)
    print("Device Name :",device_name)
    # Specify the output file name
    # Access the command-line parameter
    photo_filename = sys.argv[1]

    # Capture the photo
    capture_photo(device_name, photo_filename)

    
if __name__ == "__main__":
    main()
