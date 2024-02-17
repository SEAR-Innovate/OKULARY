import cv2
import os

def generate_dataset():
    face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(2)
    id = 1
    img_id = 0
    data_path = 'data'
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                img_id += 1
                face = gray[y:y + h, x:x + w]
                face = cv2.resize(face, (300, 300))
                file_name_path = "data/user."+str(id)+"."+str(img_id)+".jpg"
                cv2.imwrite(file_name_path, face)
                cv2.putText(face, str(img_id), (60, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Cropped face", face)
                if cv2.waitKey(1) == 13 or img_id == 200:
                    break
        if cv2.waitKey(1) == 13 or img_id == 200:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Collecting sample is completed.........")

generate_dataset()
