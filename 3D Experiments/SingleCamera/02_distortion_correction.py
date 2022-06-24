import yaml

from cam_config import *
from yaml.loader import SafeLoader

# Relevant Paths
image_path = "Chessboard_Samples/calib (22).jpg"
k_matrix_path = 'calibration_matrix.yaml'


# Method to correct distortion of a given image, knowing the camera K matrix
def undistortImage(mtx, dist, img):
    h, w = img.shape[:2]

    # Refining the camera matrix using parameters obtained by calibration
    newcamera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    # Method 1 to Undistorted the image
    dst = cv2.undistort(img, mtx, dist, None, newcamera_mtx)

    # Method 2 to undistorted the image
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcamera_mtx, (w, h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    # Displaying the undistorted image
    cv2.imshow("Undistorted Image", dst)
    cv2.waitKey(0)


# Open the file and load the file
with open(k_matrix_path) as f:
    data = yaml.load(f, Loader=SafeLoader)

mtx, dist = np.float32(data.get("camera_matrix")), np.float32(data.get("dist_coeff"))
undistortImage(mtx, dist, cv2.imread(image_path))