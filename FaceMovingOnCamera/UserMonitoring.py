import cv2
import matplotlib.pyplot as plt
import methods
import numpy as np
import dlib

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

cap = cv2.VideoCapture(0)
count = 1

while True:
    check, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            #cv2.circle(gray, (x, y), 2, (255, 0, 0), -1)

            # left eye
            eyes = gray[landmarks.part(21).y:landmarks.part(28).y,
                   landmarks.part(36).x:landmarks.part(45).x]

            eyes = cv2.Canny(eyes, 90, 150)

    cv2.imshow("Capturing", eyes)
    key = cv2.waitKey(10)

    if key == ord('q'):
        break

cap.release()
cv2.destroyWindow()