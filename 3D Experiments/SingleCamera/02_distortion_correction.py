import yaml

from cam_config import *
from yaml.loader import SafeLoader

"""
Renato Afonso - 2022
This script consists, after having calibrated the camera, perform distortion correction using the undistort method.
"""

# Relevant Paths
image_path = "Chessboard_Samples/calib (22).jpg"
k_matrix_path = 'Results/calibration_matrix.yaml'

# Method to correct distortion of a given image, knowing the camera K matrix
def undistortImage(mtx, dist, img):
    h, w = img.shape[:2]
    print(h, w)

    # Refining the camera matrix using parameters obtained by calibration
    alpha = 1
    # alpha = 0 --> returns undistorted image with min unwanted pixels
    # alpha = 1 --> pixels are retained with some extra black images
    newcamera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    # Method 1 to Undistorted the image
    dst = cv2.undistort(img, mtx, dist, None, newcamera_mtx)

    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    cv2.imwrite('Results/calibResult_method1.png', dst)

    # Method 2 to undistorted the image
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcamera_mtx, (w, h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    # crop the image
    x, y, w, h = roi
    dst_2 = dst[y:y + h, x:x + w]
    cv2.imwrite('Results/calibResult_method2.png', dst_2)

    # Displaying the undistorted image
    cv2.imshow("Undistorted Image", dst)
    cv2.waitKey(0)


# Open the file and load the file
with open(k_matrix_path) as f:
    data = yaml.load(f, Loader=SafeLoader)

mtx, dist = np.float32(data.get("camera_matrix")), np.float32(data.get("dist_coeff"))
undistortImage(mtx, dist, cv2.imread(image_path))