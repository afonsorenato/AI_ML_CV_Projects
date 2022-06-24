import os
import cv2
import glob
import numpy as np

from cam_config import *

# Vector for 3D points
threedpoints = []

# Vector for 2D points
twodpoints = []

# 3D points real world coordinates
objectp3d = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)

objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].t.RESHAPE(-1, 2)
prev_img_shape = None

# Extract path of each image stored in a directory
images = glob.glob(path + "*.jpg")

for filename in images:
    image = cv2.imread(filename)
    grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find chessboard corners
    ret, corners = cv2.findChessboardCorners(
        grayColor,
        CHECKERBOARD,
        cv2.CALIB_CB_ADAPTIVE_THRESH +
        cv2.CALIB_CB_FAST_CHECK +
        cv2.CALIB_CB_NORMALIZE_IMAGE)

    if ret == True:
        threedpoints.append(objectp3d)

        # Refine pixels coordinates
        corners2 = cv2.cornerSubPix(grayColor, corners,
                                    (11,11), (-1,-1), criteria)

        twodpoints.append(corners2)

        # Draw the displayed corners
        image = cv2.drawChessboardCorners(image,
                                          CHECKERBOARD,
                                          corners2, ret)

    cv2.imshow("Results", image)
    cv2.waitKey(0)

cv2.destroyAllWindows()

h, w = image.shape[:2]
# Perform camera calibration by
# passing the value of above found out 3D points (threedpoints)
# and its corresponding pixel coordinates of the
# detected corners (twodpoints)

ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
    threedpoints, twodpoints, grayColor.shape[::-1], None, None)

# Displaying required output
print(" Camera matrix:")
print(matrix)

print("\n Distortion coefficient:")
print(distortion)

print("\n Rotation Vectors:")
print(r_vecs)

print("\n Translation Vectors:")
print(t_vecs)


