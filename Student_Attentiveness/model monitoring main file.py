import cv2
import numpy as np
import os
import pandas as pd

atnd = []

# Train the face recognition model using the collected dataset
def train_model():
    data_path = 'data'
    face_classifier = cv2.CascadeClassifier("./Student_Attentiveness/haarcascade_frontalface_default.xml")
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
    face_classifier = cv2.CascadeClassifier("./Student_Attentiveness/haarcascade_frontalface_default.xml")
    eye_classifier = cv2.CascadeClassifier("./Student_Attentiveness/haarcascade_eye.xml")
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
        # cv2.imshow('Student Attention', frame)
        df = pd.DataFrame(atnd, columns=['Attention'])
        df.to_csv('./attention.csv')
        if cv2.waitKey(1) == 13:
            break

    cap.release()
    cv2.destroyAllWindows()

monitor_attention()
