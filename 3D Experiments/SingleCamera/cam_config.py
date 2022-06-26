import os
import cv2
import glob
import numpy as np

# Directory where the chessboard images are
path = "C:/Users/Renato/OneDrive/Documentos\GitHub\CV_Projects/3D Experiments/SingleCamera/Chessboard_Samples/"

# Define dimensions of the chessBoard
# It is the corners, not the squares
CHECKERBOARD = (8, 5)

# Stops the iteration when hits specific accuracy,
# epsilon and number of iterations
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
            30,  # iterations
            0.001)  # epsilon


def estimateReporjectionERror(objpoints, imgpoints, rvecs, tvecs, mtx, dist):
    """Re-projection error gives a good estimation of just how exact is the
    found parameters. This should be as close to zero as possible. Given the
    intrinsic, distortion, rotation and translation matrices, we first
    transform the object point to image point using cv2.projectPoints().
    Then we calculate the absolute norm between what we got with our
    transformation and the corner finding algorithm.
        """
    mean_error = 0
    tot_error = 0

    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        tot_error += error

    print("Total error: ", mean_error / len(objpoints))


