#Identifies a face and plots a rectangle around

import cv2, time

# Load the cascade
face_cascade = cv2.CascadeClassifier('haar\haarcascade_frontalface_default.xml')

# Read the input video
video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("Capturing", gray)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()
cv2.destroyWindow()

