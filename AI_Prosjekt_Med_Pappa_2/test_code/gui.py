import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Unable to read camera feed")

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Function to stream video in tkinter
def stream_video():
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret:
            frame = cv2.resize(frame, (root.winfo_width(), root.winfo_height()))
            # Convert the image from OpenCV BGR format to PIL RGB format
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)

            # Convert the Image object into a TkPhoto object
            image = ImageTk.PhotoImage(image)

            # Update the image in the label widget
            label.config(image=image)
            label.image = image

# Create a tkinter window
root = tk.Tk()

# Create a label in the tkinter window
label = tk.Label(root)
label.pack()

# Create a separate thread for the video streaming function
thread = threading.Thread(target=stream_video, daemon=True)
thread.start()

# Start the tkinter main loop
root.mainloop()

