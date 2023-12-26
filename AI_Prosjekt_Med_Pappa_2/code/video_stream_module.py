import cv2
import sys
import threading

class Video_Stream:
    def __init__(self, rtsp_link='rtsp://admin:Tesla2024!@192.168.80.80:554/h264Preview_01_sub'):
        self.rtsp_link = rtsp_link

        self.resized_frame_rel_size = 1

        self.current_frame = None
        self.current_frame_rgb = None

        self.draw_info = [None, None]

    def _video_input_not_found(self):
        sys.exit('Video source not found...')

    def _display_annotations(self, names, locations):
        
            for (top, right, bottom, left), name in zip(locations, names):
                top *= 1#(1/self.resized_frame_rel_size)
                right *= 1#(1/self.resized_frame_rel_size)
                bottom *= 1#(1/self.resized_frame_rel_size)
                left *= 1#(1/self.resized_frame_rel_size)

                cv2.rectangle(self.current_frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(self.current_frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
                cv2.putText(self.current_frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
    
    def _check_frame_call(self, queue):
        if queue.qsize() > 0:
            return queue.get()
        return False

    def get_current_frame_rgb(self):
        return self.current_frame_rgb
    
    def run(self, video_queue, video_request_queue, annotation_queue):
        self.video_input = cv2.VideoCapture(0)#self.rtsp_link)
        if not self.video_input.isOpened():
            self._video_input_not_found()
        
        while True:
            ret, frame = self.video_input.read()

            frame_call_data = self._check_frame_call(video_request_queue)
            if frame_call_data:
                video_queue.put({frame_call_data: frame})
                print('frame given')

            small_frame_bgr = cv2.resize(frame, (0,0), fx=self.resized_frame_rel_size, fy=self.resized_frame_rel_size)
            small_frame_rgb = small_frame_bgr[:, :, ::-1] # changes from bgr to rgb (color formats)

            self.current_frame = frame
            self.current_frame_rgb = small_frame_rgb

            if annotation_queue.qsize() > 0:
                annotation_data = annotation_queue.get()
                self._display_annotations(annotation_data[0], annotation_data[1])

            cv2.imshow('Face Recognition', self.current_frame)

            if cv2.waitKey(1) == ord('q'):
                break
