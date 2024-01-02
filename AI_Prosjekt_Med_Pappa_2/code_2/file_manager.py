import os
import json

from utils import path_exists

class File_Manager:
    def __init__(self):
        self.image_formats = ('.png', '.jpeg', '.jpg')

    def load_json_file(self, path: str) -> any:
        if not path_exists(path):
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{path}'")
        
        try:
            with open(path) as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"An error occurred while parsing the JSON file: {path}. Error: {str(e)}")

    def load_directory_image_paths(self, path: str) -> list:
        if not path_exists(path):
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{path}'")
        
        image_paths = []
        for root, dirs, files in os.walk(path):
            for file_name in files: # type: str
                if file_name.endswith(self.image_formats):
                    image_path = os.path.join(root, file_name)
                    image_normpath = os.path.normpath(image_path)
                    image_paths.append(image_normpath)
        return image_paths
    
    def create_cache(self, file_name: str, data: list | dict, path: str) -> None:
        if not path_exists(path):
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{path}'")
        
        try:
            with open(f'{path}/{file_name}.json', 'w') as file:
                json.dump(data, file)
        except IOError as e:
            raise Exception(f"An error occurred while creating the cache: {e}")
        
    def load_cache(self, path: str) -> any:
        return self.load_json_file(path)
    
    def delete_file(self, path: str) -> None:
        if not path_exists(path):
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{path}'")
        
        if os.path.isfile(path):
            try:
                os.remove(path)
            except OSError as e:
                raise Exception(f'Error: {e.strerror}')

