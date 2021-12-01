import os
import dlib

import cv2
import time


predictor_path = os.path.join("shape_predictor_68_face_landmarks.dat")
predictor = dlib.shape_predictor(predictor_path)
detector = dlib.get_frontal_face_detector()
cap = cv2.VideoCapture(0)

while True:
    suc, frame = cap.read()
    faces = detector(frame)

    if faces:
        landmarks = predictor(frame, faces[0])

        for i in range(0,68):
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)



    #frame = cv2.resize(frame, (round(frame.shape[1]/1.4), round(frame.shape[0]/1.4)))
    cv2.imshow("Live", frame)
    cv2.waitKey(1)

