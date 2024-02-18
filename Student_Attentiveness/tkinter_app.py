import cv2
import numpy as np
import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

atnd = []

# Train the face recognition model using the collected dataset
def train_model():
    data_path = 'data'
    face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    training_data = []
    labels = []

    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith('jpg'):
                path = os.path.join(root, file)
                label = int(path.split('.')[1])
                image = cv2.imread(path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                face = face_classifier.detectMultiScale(gray, 1.3, 5)
                if face is not ():
                    for (x, y, w, h) in face:
                        cropped_face = gray[y:y + h, x:x + w]
                        training_data.append(cropped_face)
                        labels.append(label)

    labels = np.array(labels)
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(training_data, labels)

    return model

# Implement the student attention monitoring system
def monitor_attention():
    global atnd
    atnd = []
    face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    eye_classifier = cv2.CascadeClassifier("haarcascade_eye.xml")
    model = train_model()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        if faces is not ():
            for (x, y, w, h) in faces:
                cropped_face = gray[y:y + h, x:x + w]
                label, confidence = model.predict(cropped_face)
                if confidence < 100:
                    eyes = eye_classifier.detectMultiScale(cropped_face)
                    if eyes is not ():
                        for (ex, ey, ew, eh) in eyes:
                            atnd.append(1)
                    else:
                        atnd.append(0)
        cv2.imshow('Student Attention', frame)
        if cv2.waitKey(1) == 13:
            break

    cap.release()
    cv2.destroyAllWindows()
    save_attendance()

def save_attendance():
    df = pd.DataFrame(atnd, columns=['Attention'])
    df.to_csv('./attention.csv')
    messagebox.showinfo("Attendance Saved", "Attendance data has been saved successfully.")

def start_monitoring():
    monitor_attention()

def stop_monitoring():
    messagebox.showinfo("Monitoring Stopped", "Monitoring has been stopped.")

def main():
    root = tk.Tk()
    root.title("Student Attentiveness")

    video_frame = tk.Label(root)
    video_frame.pack()

    start_button = tk.Button(root, text="Start Monitoring", command=start_monitoring)
    start_button.pack()

    stop_button = tk.Button(root, text="Stop Monitoring", command=stop_monitoring)
    stop_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
