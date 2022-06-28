import cv2
import glob
import numpy as np


chessboardSize = (6,7)
frameSize = (1280, 1000)


# Termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
            30, 0.001)

# Prepare object points
objp = np.zeros((chessboardSize[0]*chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],
             0:chessboardSize[1]].T.reshape(-1,2)

objp = objp*20

