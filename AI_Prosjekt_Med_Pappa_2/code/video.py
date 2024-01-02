import cv2

video_input = cv2.VideoCapture('rtsp://admin:Tesla2024!@10.0.0.38:554/h264Preview_01_main')
while True:
    ret, frame = video_input.read()

    cv2.imshow('Face Recognition', frame)

    if cv2.waitKey(1) == ord('q'):
        break