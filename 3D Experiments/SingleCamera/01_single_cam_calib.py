import os
import cv2
import glob
import yaml
import numpy as np

from cam_config import *

# Vector for 2D and 3D points
threeD_points = []
twoD_points = []

# 3D points real world coordinates
objectp3d = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

# Extract path of each image stored in a directory
images = glob.glob(path + "*.jpg")

for filename in images:
    image = cv2.imread(filename)
    grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find chessboard corners (corners coordinate in pixels)
    status, corners = cv2.findChessboardCorners(
        grayColor, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

    # If 2d points are found, refine them
    if status:
        # Saves the 3D points
        threeD_points.append(objectp3d)
        # Refine pixels coordinates
        corners2 = cv2.cornerSubPix(grayColor, corners, (11, 11), (-1, -1), criteria)
        # Saves thr 2D points
        twoD_points.append(corners2)
        # Draw the displayed corners
        image = cv2.drawChessboardCorners(image, CHECKERBOARD, corners2, status)

    cv2.imshow("Results", cv2.resize(image, (800, 600)))
    cv2.waitKey(0)

cv2.destroyAllWindows()

# Perform camera calibration by passing the value of above found out 3D points (threedpoints)
# and its corresponding pixel coordinates of the detected corners (twoD_points)
status, mtx, dist, r_vecs, t_vecs = cv2.calibrateCamera(threeD_points, twoD_points, grayColor.shape[::-1], None, None)

# Returns the re-projection error
estimateReporjectionERror(objectp3d, twoD_points, r_vecs, t_vecs, mtx, dist)

# Displaying required output
print(" Camera mtx:", str(mtx))
print("\n Distortion coefficient:", str(dist))
print("\n Rotation Vectors:", str(r_vecs))
print("\n Translation Vectors:", str(t_vecs))

# transform the mtx and dist coefficients to writable lists
data = {'camera_matrix': np.asarray(mtx).tolist(),
        'dist_coeff': np.asarray(dist).tolist()}

# and save it to a file
with open("calibration_matrix.yaml", "w") as f:
    yaml.dump(data, f)