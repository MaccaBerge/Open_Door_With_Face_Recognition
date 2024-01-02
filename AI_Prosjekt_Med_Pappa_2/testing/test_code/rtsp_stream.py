import cv2

# Create a named window
cv2.namedWindow("Webcam Feed")

# Capture video from the default camera
vc = cv2.VideoCapture('rtsp://admin:Tesla2024!@192.168.80.80:554/h264Preview_01_main')

# Check if the camera is opened correctly
if not vc.isOpened():
    raise IOError("Cannot open webcam")

# Loop through the frames and display them
while True:
    # Read the frame
    rval, frame = vc.read()

    # Show the frame in the window
    cv2.imshow("Webcam Feed", frame)

    # Exit the loop on pressing the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and destroy the window
vc.release()
cv2.destroyAllWindows()