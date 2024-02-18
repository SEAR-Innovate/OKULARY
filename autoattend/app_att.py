import tkinter as tk
from tkinter import ttk
import cv2
import face_recognition
import numpy as np
from datetime import datetime
<<<<<<< HEAD
import os


root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("800x600")


video_frame = tk.Frame(root)
video_frame.pack(pady=20)


video_label = tk.Label(video_frame)
video_label.pack()


def start_video_feed():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(frame)
        for face in faces:
            top, right, bottom, left = face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.resize(frame, (800, 600))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        video_label.update()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def stop_video_feed():
    root.quit()


start_button = ttk.Button(root, text="Start", command=start_video_feed)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = ttk.Button(root, text="Stop", command=stop_video_feed)
stop_button.pack(side=tk.LEFT, padx=10)


=======
import pickle
import tkinter as tk
from PIL import Image, ImageTk

# Function to start face recognition
def start_recognition():
    global is_recognizing
    is_recognizing = True
    # Start video capture
    cap = cv2.VideoCapture(0)
    while is_recognizing:
        success, img = cap.read()
        imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faces_in_frame = face_recognition.face_locations(imgS)
        encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
        for encode_face, faceloc in zip(encoded_faces, faces_in_frame):
            matches = face_recognition.compare_faces(encoded_face_train, encode_face)
            faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
            matchIndex = np.argmin(faceDist)
            print(matchIndex)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper().lower()
                y1, x2, y2, x1 = faceloc
                # since we scaled down by 4 times
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)
        # Display the video feed
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        panel.imgtk = imgtk
        panel.configure(image=imgtk)
        panel.update()
    cap.release()

# Function to stop face recognition
def stop_recognition():
    global is_recognizing
    is_recognizing = False

# Initialize tkinter window
root = tk.Tk()
root.title("Auto Attendance")

# Create a label for the title
title_label = tk.Label(root, text="Auto Attendance")
title_label.pack(pady=5)

# Create a panel to display video feed
panel = tk.Label(root)
panel.pack(padx=10, pady=10)

# Create start and stop buttons
start_button = tk.Button(root, text="Start", command=start_recognition)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop", command=stop_recognition)
stop_button.pack(pady=5)

# Load images and initialize variables
path = './autoattend/photos'
images = []
classNames = []
mylist = os.listdir(path)
for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

# Encode faces
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList

encoded_face_train = findEncodings(images)

# Function to mark attendance
def markAttendance(name):
    with open('./autoattend/Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            time = now.strftime('%I:%M:%S:%p')
            date = now.strftime('%d-%B-%Y')
            f.writelines(f'n{name}, {time}, {date}')

# Set is_recognizing flag
is_recognizing = False

>>>>>>> 75440fa3805bca07da8c622c82c716fdaef120fb
root.mainloop()
