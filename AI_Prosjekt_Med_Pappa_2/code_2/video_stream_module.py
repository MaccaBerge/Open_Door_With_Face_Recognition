import cv2
import sys


class Video_Stream:
    def __init__(self, video_input='rtsp://admin:Tesla2024!@10.0.0.38:554/h264Preview_01_sub'):
        self.video_input = video_input
        self.video_capture = cv2.VideoCapture(self.video_input)

        if not self.video_capture.isOpened():
            self._video_capture_not_found()

        self.resized_frame_rel_size = 1

        self.current_frame = None
        self.current_frame_rgb = None

        self.draw_info = [None, None]

    def _video_capture_not_found(self):
        self.video_capture = cv2.VideoCapture(self.video_input)
        if not self.video_capture.isOpened():
            self._video_capture_not_found()
        #sys.exit('Video source not found...')

    def _display_annotations(self, names, locations):
        
        for (top, right, bottom, left), name in zip(locations, names):
            top *= 4#(1/self.resized_frame_rel_size)
            right *= 4#(1/self.resized_frame_rel_size)
            bottom *= 4#(1/self.resized_frame_rel_size)
            left *= 4#(1/self.resized_frame_rel_size)

            cv2.rectangle(self.current_frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(self.current_frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
            cv2.putText(self.current_frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

    def get_current_frame_rgb(self):
        return self.current_frame_rgb
    
    def run(self):
        while True:
            try:
                ret, frame = self.video_capture.read()

                small_frame_bgr = frame#cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
                small_frame_rgb = small_frame_bgr[:, :, ::-1] # changes from bgr to rgb (color formats)

                self.current_frame = frame
                self.current_frame_rgb = small_frame_rgb

                cv2.imshow('Face Recognition', self.current_frame)

                if cv2.waitKey(1) == ord('q'):
                    break
            except Exception as e:
                print(f'An error occurd with the video stream: {e}')




# import threading


# video = Video_Stream('rtsp://admin:Tesla2024!@10.0.0.38:554/h264Preview_01_main')

# video_thread = threading.Thread(target=video.run)
# video_thread.start()