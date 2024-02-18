import tkinter as tk
from tkinter import ttk
import cv2
import face_recognition
import numpy as np
from datetime import datetime
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


root.mainloop()
