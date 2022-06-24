import os
import cv2
import glob
import numpy as np


# Directory where the chessboard images are
path = "C:\Users\Renato\OneDrive\Documentos\GitHub\CV_Projects" \
       "/3D Experiments/SingleCamera/Chessboard_Samples/"

# Define dimensions of the chessBoard
CHECKERBOARD = (6, 9)

# Stops the iteration when hits specific accuracy,
# epsilon and number of iterations
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
            30,         #iterations
            0.001)      #epsilon


