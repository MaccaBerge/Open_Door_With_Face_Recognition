import os
from numpy import ndarray, array
import multiprocessing

from file_manager import File_Manager
from utils import load_face_recognition_image
from utils import encode_face_recognition_image


class Data:
    def __init__(self, config_path: str):
        self.file_manager = File_Manager()

        self.config_paths = self.file_manager.load_json_file(config_path)

        self.data = {}

        self._setup()
        print(self.data)
    
    def _setup(self) -> None:
        self.caches = self._load_caches(os.path.normpath(self.config_paths.get('caches')))
        print('caches: ', self.caches)

        if 'face_encodings.json' not in self.caches:
            face_image_paths = self.file_manager.load_directory_image_paths(self.config_paths['faces'])
            face_images, self.face_names = self._load_face_images(face_image_paths)
            self.encoded_face_images = self._encode_images_pool(face_images)
            #self.encoded_face_images = self._encode_images(face_images)

            self.file_manager.create_cache('face_encodings', [array[0].tolist() for array in self.encoded_face_images], self.config_paths['caches'])
            self.file_manager.create_cache('face_names', self.face_names, self.config_paths['caches'])

            self.data['face_encodings'] = self.encoded_face_images
            self.data['face_names'] = self.face_names
            return 
        
        self.data['face_encodings'] = [array(list) for list in self.caches['face_encodings.json']]
        self.data['face_names'] = self.caches['face_names.json']
  
    def _load_face_images(self, image_paths: list[str]) -> tuple[list, list]:
        face_images = []
        face_names = []
        for image_path in image_paths:
            face_name = image_path.split(os.sep)[-2]
            face_names.append(face_name)
            try:
                image = load_face_recognition_image(image_path)
                face_images.append(image)
                print(image_path)
            except FileNotFoundError:
                print(f"Warning: File not found for image path: {image_path}")
                return []
            except Exception as e:
                print(f"Error loading image at {image_path}: {e}")

        return face_images, face_names
    
    def _encode_images_pool(self, images: list[ndarray]) -> list[ndarray]:
        with multiprocessing.Pool() as pool:
            results = pool.map(self._encode_image, images)
            print(results)
            return results
    
    def _encode_image(self, image):
        return encode_face_recognition_image(image, num_jitters=30)
    
    def _encode_images(self, images: list[ndarray]) -> list[ndarray]:
        try:
            num_images = len(images)
            encoded_images = []
            for index, image in enumerate(images):
                print(f'Encoding image: {index+1}/{num_images}')
                encoded_image = encode_face_recognition_image(image, num_jitters=30)
                encoded_images.append(encoded_image)
            return encoded_images
        except Exception as e:
            print(f'Failed to encode image {index+1}/{num_images}: {e}')
            return []

    def _load_caches(self, cache_directory: str) -> dict:
        caches = {}
        for file_name in os.listdir(cache_directory):
            file_path = os.path.join(cache_directory, file_name)
            file_data = self.file_manager.load_cache(file_path)
            caches[file_name] = file_data
        return caches


if __name__ == '__main__':
    data = Data('../config.json')