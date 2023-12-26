import cv2
import face_recognition
from multiprocessing.pool import ThreadPool

# Create a VideoCapture object to read the video stream
cap = cv2.VideoCapture('rtsp://admin:Tesla2024!@192.168.80.80:554/h264Preview_01_sub')

# Load the known faces and their names
known_faces = [
    face_recognition.load_image_file('faces_test/andreas.png'),
    face_recognition.load_image_file('faces_test/marcus.png'),
    face_recognition.load_image_file('faces_test/bard.png')
]
known_names = ['andreas', 'marcus', 'bard']

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

# Create a thread pool with 4 threads
pool = ThreadPool(processes=4)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    if not ret:
        break

    # Find all the faces and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Initialize an array for the names of the detected faces
    face_names = []

    # Create a list of tasks to process the face encodings
    tasks = []
    for face_encoding in face_encodings:
        task = pool.apply_async(face_recognition.compare_faces, (known_faces, face_encoding))
        tasks.append(task)

    # Loop through each task and get the name of the detected face
    for i, task in enumerate(tasks):
        matches = task.get()
        if True in matches:
            name = known_names[matches.index(True)]
        else:
            name = 'Unknown'
        face_names.append(name)

    # Draw rectangles around the detected faces and label them with their names
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Wait for a key press before processing the next frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()

