import cv2

def list_video_devices():
    # Try to open video capture for each device index from 0 to 10
    for i in range(10):
        cap = cv2.VideoCapture(i)
        
        # Check if the camera is opened successfully
        if cap.isOpened():
            print(f"Device {i}: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
            cap.release()
        else:
            break

if __name__ == "__main__":
    print("List of available video devices:")
    list_video_devices()
