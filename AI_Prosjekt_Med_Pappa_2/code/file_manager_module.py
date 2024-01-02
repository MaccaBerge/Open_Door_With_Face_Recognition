import os
import json
import time
import numpy as np

class File_Manager:
    def __init__(self):
        self.cache_file_paths = {
        'face_encodings': 'caches/face_encodings.json',
        'face_names': 'caches/face_names.json',
        'last_modified': 'caches/last_modified.json', 
        }

        self.paths = {
            'persons': 'faces'
        }

        self.new_files = None

        if not os.path.exists(self.cache_file_paths['last_modified']):
            self.create_cache([time.time()], 'last_modified')
        else:
            self.new_files = self.get_new_files('faces')
            self.update_cache([time.time()], self.cache_file_paths['last_modified'], overwrite=True)

    def create_cache(self, data: list, file_name: str, path: str ='caches') -> None:
        try:
            os.makedirs(path, exist_ok=True)
            with open(f'{path}/{file_name}.json', 'w') as file:
                json.dump(data, file)
        except Exception as e:
            print(f"An error occurred while creating the cache: {e}")

    def update_cache(self, new_data: list, path: str, overwrite=False) -> None:
        if not self.cache_exist(path):
            raise ValueError(f"Cache does not exist at {path}")
        
        with open(path, 'r') as file:
            data = list(json.load(file))
        
        if overwrite:
            data = new_data
        else: 
            data.extend(new_data)

        with open(path, 'w') as file:
            json.dump(data, file)

    def load_cache(self, path: str, ndarray=False) -> list:
        try:
            with open(path, 'r') as file:
                data = list(json.load(file))
            if ndarray:
                return [np.array(element) for element in data]
        except:
            return None
        return data

    def cache_exist(self, path) -> bool:
        return os.path.exists(path)
    
    def get_new_files(self, directory_path: str) -> list:
        try:
            last_modified_time = float(self.load_cache(self.cache_file_paths['last_modified'])[-1])
        except Exception as e:
            print(f"An error occurred while loading the cache: {e}")
            return []
        
        new_files = []
        try:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_modified_time = os.path.getmtime(file_path)

                    if file_modified_time > last_modified_time:
                        new_files.append(file_path)
        except Exception as e:
            print(f"An error occurred while loading the cache: {e}")
        
        return new_files
    
    def ndarry_to_list(self, ndarray):
        return [array.tolist() for array in ndarray]
