import cv2
import numpy as np
import time
import imutils
import methods

#Estimate distance to an object (then, to the face)
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
count = 1
w = 0

while 1:

    check, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    #Draws rectangle with my face
    for (x, y, w, h) in faces:
        gray = cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 0, 255), 2)

    #-----second part---------------------------------------------------
    if w > 0:
        width_faceInPixels = w #Width of my face (just testing)
        width_faceInCM = 15 #cm
        fl = 812/2
        count += 1

        if count > 10:
            dist = width_faceInCM*fl/width_faceInPixels
            print("Width pixels: " + str(round(width_faceInPixels)))
            print(str(round(dist)) + "cm")
            count = 0

    cv2.imshow("Output", gray)
    key = cv2.waitKey(20)
    if key == ord('q'):
        break
