import face_recognition
import os
from numpy import ndarray


def path_exists(path: str) -> bool:
    return os.path.exists(path)

def load_face_recognition_image(path: str) -> ndarray:
    if not os.path.exists(path):
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{path}'")
    
    try:
        return face_recognition.load_image_file(path)
    except Exception as e:
        raise RuntimeError(f'An error occurd while loading the image: {e}')

def encode_face_recognition_image(image: ndarray, num_jitters: int=1) -> list[ndarray]:
    return face_recognition.face_encodings(image, num_jitters=num_jitters)

