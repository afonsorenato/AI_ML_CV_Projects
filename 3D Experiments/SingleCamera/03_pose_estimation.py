import glob
import cv2 as cv
import numpy as np

from cam_config import *

"""
This script gets a live streaming from the webcam and, if a chessboard (8x5) is placed on sight, it will draw a 3D 
cartesian axis system to estimate the plane's pose.
"""

# Some initial configuration
objp = np.zeros((CHECKERBOARD[1] * CHECKERBOARD[0], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
axis = np.float32([[3, 0, 0], [0, 3, 0], [0, 0, -3]]).reshape(-1, 3)

# Captures video from webcam
cap = cv.VideoCapture(0)

while True:

    # Get img sample from webcam
    ok, img = cap.read()

    if not ok:
        break

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        # Minimizes the re-projection error assuming sub-pixel precision
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # Find the rotation and translation vectors.
        ret, r_vector, t_vector = cv.solvePnP(objp, corners2, mtx, dist)

        # project 3D points to image plane
        imgpts, jac = cv.projectPoints(axis, r_vector, t_vector, mtx, dist)
        img = draw(img, corners2, imgpts)

    cv.namedWindow("Result", cv.WINDOW_NORMAL)
    cv.imshow('Result', cv2.resize(img, (800, 600)))
    cv.waitKey(1)

