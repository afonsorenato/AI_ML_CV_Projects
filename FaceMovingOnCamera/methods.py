import cv2
import numpy as np
import time
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from itertools import product, combinations


# returns the name of the file with chessboard
def getName(i):
    aux = "chessboards\chess"
    aux2 = str(i + 1)
    aux3 = ".jpg"

    name = aux + aux2 + aux3

    return name

# return the relation points real and in frame w/ chesssboard
def getCalibPoints(objpoints, imgpoints, objp):
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    for i in range(15):

        name = getName(i)
        print(name)

        img = cv2.imread(name, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            # print(corners2)
            imgpoints.append(corners2)

            # Draw and display the corners
            # img = cv2.drawChessboardCorners(img, (7, 6), corners2, ret)
            # cv2.imshow('img', img)
            # cv2.waitKey(500)

    return objpoints, imgpoints, objp, gray

# print camera intrinsic parameters
def printIntrinsics(mtx):
    fl1 = str(round(mtx[0][0]))
    fl2 = str(round(mtx[1][1]))
    fl = fl1 + ", " + fl2

    oc1 = str(round(mtx[0][2]))
    oc2 = str(round(mtx[1][2]))
    oc = oc1 + ", " + oc2

    print("Intrinsic parameters: ")
    print(mtx)
    print("Focal length: (" + fl + ") pix")
    print("Optical center: (" + oc + ") pix")

    return fl1

# eye-box volume at a certain distance from camera
def drawEyeBoxSize(faceDist, img):

    #Assumed eye-box size at camera's position (0,0,0)
    init_width = 160 #130
    init_hight = 70  #60

    ratio_per_cm = 0.5
    w = int(init_width - ratio_per_cm * faceDist)
    h = int(init_hight - ratio_per_cm * faceDist)

    width, height = img.shape[:2]
    x = int(width/2)
    y = int(height/2-h)

    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    aux = "Dist from camera: " + str(faceDist) + " cm"
    cv2.putText(img, aux, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
    cv2.putText(img, 'HUD Eye-box', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)

    return x, y, w, h

# Get calibration position in eye-box
def printCalibPosition(centroid_eye_left, img, a, b, c, d, x, y, ex, ey, ew, eh):

    if ((a < (ex + x) and (x + ex + ew > a)) and (a + c > (ex + x) and (x + ex + ew < a + c))) and (
            (b < (ey + y) and (y + ey + eh > b)) and (b + d > (ey + y) and (y + ey + eh < b + d))):
        cv2.putText(img, 'Driver inside the Eye-box', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 20, 12), 1)

        if (centroid_eye_left[0] > a) and (centroid_eye_left[0] < a + c / 3):
            cv2.putText(img, 'Position C1', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
        elif (centroid_eye_left[0] >= a + c / 3) and (centroid_eye_left[0] < a + c / 3 * 2):
            cv2.putText(img, 'Position C2', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
        elif (centroid_eye_left[0] >= a + c / 3 * 2) and (centroid_eye_left[0] < a + c):
            cv2.putText(img, 'Position C3', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

    else:
        cv2.putText(img, 'Driver outside the Eye-box', (350, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 25, 12), 1)

    return

def printCalibPositionDlib(img,centroid, x_left_eye, x_right_eye, a, b, c):

    if (a < x_left_eye and x_right_eye < a+c):
        cv2.putText(img, 'Driver inside the Eye-box', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 20, 12), 1)

        if (centroid > a) and (centroid < a + c / 3):
            cv2.putText(img, 'Position C1', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
        elif (centroid >= a + c / 3) and (centroid < a + c / 3 * 2):
            cv2.putText(img, 'Position C2', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
        elif (centroid >= a + c / 3 * 2) and (centroid < a + c):
            cv2.putText(img, 'Position C3', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
    else:
        cv2.putText(img, 'Driver outside the Eye-box', (350, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 25, 12), 1)

    return

#Estimate distance from face - camera
def getFaceDist(w, face_ref):
    width_faceInPixels = w  # Width of my face (just testing)
    width_faceInCM = face_ref  # cm
    fl = 812 / 2

    dist = round(width_faceInCM * fl / width_faceInPixels)
    #print("width pixels: " + str(round(width_faceInPixels)))
    aux_str = "Dist from camera: " + str(dist) + "cm"
    print(aux_str)

    return dist


################################################

def getDrowsiness(landmarks, img):






    return
