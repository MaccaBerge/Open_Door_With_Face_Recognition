import face_recognition
import os
import numpy as np
import math
import threading

from file_manager_module import File_Manager

class Face_Recognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self, video_object):
        self.video_object = video_object
        self.file_manager = File_Manager()

        self._setup()
        self.frame = None
    
    def _setup(self) -> None:
        if self.file_manager.cache_exist(self.file_manager.cache_file_paths['face_encodings']):
            print('|CACHE FOUND|')
            new_images = self.file_manager.new_files
            if new_images:
                print('|NEW FILES DETECTED|')
                encoded_faces_info = self._encode_new_faces(new_images)
                names, encoded_faces = zip(*encoded_faces_info)
                print(list(encoded_faces))
                print('|UPDATING CACHES|')
                self.file_manager.update_cache(names, self.file_manager.cache_file_paths['face_names'])
                self.file_manager.update_cache(self.file_manager.ndarry_to_list(list(encoded_faces)[0]), self.file_manager.cache_file_paths['face_encodings'])
                print('|CHACHES UPDATED|')
            else:
                print('|NO NEW FILES DETECTED|')
        else:
            self._encode_all_faces()
            self.file_manager.create_cache(self.file_manager.ndarry_to_list(self.known_face_encodings), 'face_encodings')
            self.file_manager.create_cache(self.known_face_names, 'face_names')
        
        print('|LOADING CACHES|')
        self.known_face_encodings = self.file_manager.load_cache(self.file_manager.cache_file_paths['face_encodings'], ndarray=True)
        self.known_face_names = self.file_manager.load_cache(self.file_manager.cache_file_paths['face_names'])
        print('|SUCCECFULLY LOADED CACHES|')
    
    def _encode_face(self, image_path) -> np.ndarray:
        print(f'|ENCODING IMAGE| -> {image_path.split()[-1]}')
        face_image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(face_image)[0]
        return face_encoding
    
    def _encode_new_faces(self, new_images: list) -> list:
        print(f'|ENCODING NEW IMAGES| -> {new_images}')
        encoded_faces = []
        for image_path in new_images:
            name = image_path.split("\\")[-2]
            face_image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face_image)
            encoded_faces.append([name, face_encoding])
        
        return encoded_faces

    def _encode_all_faces(self):
        for person in os.listdir(self.file_manager.paths['persons']):
            for image_name in os.listdir(f'{self.file_manager.paths["persons"]}/{person}'):
                try:
                    face_encoding = self._encode_face(f'{self.file_manager.paths["persons"]}/{person}/{image_name}')
                    self.known_face_names.append(person)
                    self.known_face_encodings.append(face_encoding)
                    print(f'{image_name} |ENCODED|')
                except:
                    print(f'{image_name} |ERROR: NO FACE DETECTED|')

    def _get_face_confidence(self, face_distance, face_match_threshold=0.6):
        range = (1.0 - face_match_threshold)
        linear_value = (1.0 - face_distance) / (range * 2.0)

        if face_distance > face_match_threshold:
            return str(round(linear_value * 100, 2)) + '%'
        else:
            value = (linear_value + ((1.0 - linear_value) * math.pow((linear_value - 0.5) * 2, 0.2))) * 100
            return str(round(value, 2)) + '%'

    def _reccive_frame(self, queue, process_id):
        if queue.qsize() <= 0:
            return None
        data: dict = queue.get()
        if data.get(process_id) is not None:
            return data[process_id]
        return None

    def process_run(self, process_id, video_queue, video_request_queue, annotation_queue):
        frame = None
        print(process_id)
        
        while True:
            print('running...', process_id)
            video_request_queue.put(process_id)
            while frame is None:
                frame = self._reccive_frame(video_queue, process_id)

            #print(process_id)
            # Find all the faces
            self.face_locations = face_recognition.face_locations(frame)
            self.face_encodings = face_recognition.face_encodings(frame, self.face_locations)

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
                
                self.face_names.append(f'{name} ({confidence})')
                print(self.face_names)
            annotation_queue.put((self.face_names, self.face_locations))