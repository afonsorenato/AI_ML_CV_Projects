import os
import cv2
import yaml
import glob
import numpy as np

from yaml.loader import SafeLoader

# Directory where the chessboard images are
path = "C:/Users/Renato/OneDrive/Documentos\GitHub\CV_Projects/3D Experiments/SingleCamera/Chessboard_Samples/"

# File with camera parameters
k_matrix_path = 'calibration_matrix.yaml'

# Define dimensions of the chessBoard
# It is the corners, not the squares
CHECKERBOARD = (8, 5)

# Colors and Draws
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)

lINE_THICKNESS = 5
FONT = cv2.FONT_HERSHEY_SIMPLEX

# Stops the iteration when hits specific accuracy,
# epsilon and number of iterations
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
            30,  # iterations
            0.001)  # epsilon

# Open the file and load the file
with open(k_matrix_path) as f:
    data = yaml.load(f, Loader=SafeLoader)

mtx, dist = np.float32(data.get("camera_matrix")), np.float32(data.get("dist_coeff"))


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


def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), BLUE, lINE_THICKNESS)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), GREEN, lINE_THICKNESS)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), RED, lINE_THICKNESS)
    return img


def drawCube(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1, 2)
    # draw ground floor in green
    img = cv2.drawContours(img, [imgpts[:4]], -1, GREEN, -3)

    # draw pillars in blue color
    for i, j in zip(range(4), range(4, 8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (255), 3)

    # draw top layer in red color
    img = cv2.drawContours(img, [imgpts[4:]], -1, RED, 3)

    return img
