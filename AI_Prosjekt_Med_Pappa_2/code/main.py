import multiprocessing
import os

from face_recognition_module import Face_Recognition
from video_stream_module import Video_Stream


if __name__ == '__main__':
    video_stream_object = Video_Stream()
    face_recognition_object = Face_Recognition(video_stream_object)

    video_queue = multiprocessing.Queue()
    veideo_request_queue = multiprocessing.Queue()

    annotation_queue = multiprocessing.Queue()
    annotation_request_queue = multiprocessing.Queue()

    video_process = multiprocessing.Process(target=video_stream_object.run, args=(video_queue, veideo_request_queue, annotation_queue))
    video_process.start()

    for process_id in range(os.cpu_count() - 1):
        face_recognition_process = multiprocessing.Process(target=face_recognition_object.process_run, args=(process_id, video_queue, veideo_request_queue, annotation_queue))
        face_recognition_process.start()

    
    