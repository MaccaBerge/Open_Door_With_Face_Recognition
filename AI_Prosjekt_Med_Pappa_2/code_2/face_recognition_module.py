import face_recognition
import numpy as np
import math
import threading

from open_door import Open_Door

class Face_Recognition:
    face_locations = []
    face_encodings = []
    face_names = []
    process_current_frame = True

    def __init__(self, video_object, data: dict):
        self.video_object = video_object
        self.data = data

        self.open_door_object = Open_Door()

        self.known_face_encodings = self.data['face_encodings']
        self.known_face_names = self.data['face_names']

    def _get_face_confidence(self, face_distance, face_match_threshold=0.6):
        range = (1.0 - face_match_threshold)
        linear_value = (1.0 - face_distance) / (range * 2.0)

        if face_distance > face_match_threshold:
            return str(round(linear_value * 100, 2)) + '%'
        else:
            value = (linear_value + ((1.0 - linear_value) * math.pow((linear_value - 0.5) * 2, 0.2))) * 100
            return str(round(value, 2)) + '%'

    def run(self):
        while True:
            frame = None
            while frame is None:
                frame = self.video_object.get_current_frame_rgb()
            frame = np.array(frame)
            # Find all the faces
            self.face_locations = face_recognition.face_locations(frame)
            self.face_encodings = face_recognition.face_encodings(frame, known_face_locations=self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = 'Unknown'
                confidence = '???'

                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    confidence = self._get_face_confidence(face_distances[best_match_index])
                    open_door_thread = threading.Thread(target=self.open_door_object.send_open_door_request)
                    open_door_thread.start()
                
                self.face_names.append(f'{name} ({confidence})')

                print(self.face_names)
