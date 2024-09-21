import sys
import cv2

def capture_photo(device_name, photo_filename='captured_photo.jpg'):
    # Open the video capture device
    cap = cv2.VideoCapture(device_name)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2592)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not capture frame.")
        cap.release()
        return

    # Save the captured frame as an image file
    cv2.imwrite(photo_filename, frame)

    # Release the capture device
    cap.release()
    print("Photo captured and saved ")

def main():
    # Check the number of command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python shot.py <nomefile.jpg>")
        sys.exit(1)

    # Access the command-line parameter
    photo_filename = sys.argv[1]

    # Your program logic here
    #print(f"The parameter passed is: {parameter}")
    # Specify the device index and photo filename (modify as needed)
    device_name = "video0"  # Check which device index your camera is using (e.g., /dev/video2)
    # Capture the photo
    capture_photo(device_name, photo_filename)

    
if __name__ == "__main__":
    main()




