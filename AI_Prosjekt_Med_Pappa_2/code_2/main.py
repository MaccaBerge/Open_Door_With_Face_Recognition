import threading

from data import Data
from video_stream_module import Video_Stream
from face_recognition_module import Face_Recognition

class Main:
    def __init__(self):
        self.config_path = '../config.json'
        self.data_class = Data(self.config_path)
        print('Data class setup complete!')

        self.rtsp_link = 'rtsp://admin:Tesla2024!@10.0.0.38:554/h264Preview_01_main'
        self.video_stream = Video_Stream(video_input=self.rtsp_link)

        self.face_recognition = Face_Recognition(self.video_stream, self.data_class.data)

        self.video_stream_thread = threading.Thread(target=self.video_stream.run)
        self.face_recognition_thread = threading.Thread(target=self.face_recognition.run)
    
    def run(self):
        self.video_stream_thread.start()
        self.face_recognition_thread.start()


if __name__ == '__main__':
    main = Main()
    main.run()
