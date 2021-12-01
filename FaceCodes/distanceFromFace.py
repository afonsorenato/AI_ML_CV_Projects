import cv2
import numpy as np
import time
import methods
import imutils

face_cascade = cv2.CascadeClassifier('haar\haarcascade_frontalface_default.xml')

#camera focal length
#size of image sensor

#calibrate camera with chessboard
"""
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane

objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)*3  # square size = 3mm

#Camera calibration
objpoints, imgpoints, objp, gray = methods.getCalibPoints(objpoints, imgpoints, objp)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
"""

cap = cv2.VideoCapture(0)
count = 1
aux_str = ""

while 1:

    check, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    #Draws rectangle with my face
    for (x, y, w, h) in faces:
        gray = cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 0, 255), 2)

    #-----second part---------------------------------------------------
    width_faceInPixels = w #Width of my face (just testing)
    width_faceInCM = 15 #cm
    fl = 812/2
    count += 1

    if count > 10:
        dist = width_faceInCM*fl/width_faceInPixels
        print("width pixels: " + str(round(width_faceInPixels)))
        aux_str = "Dist from camera: " + str(round(dist)) + "cm"
        print(aux_str)
        count = 0

    cv2.putText(gray, aux_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    cv2.imshow("Canny gray image", gray)
    key = cv2.waitKey(20)
    if key == ord('q'):
        break
