import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

imgL = cv.imread('Samples/left.jpg', 0)
imgR = cv.imread('Samples/right.jpg', 0)

# Estimate the stereo disparity
stereo = cv.StereoBM_create(numDisparities=16, blockSize=13)
disparity = stereo.compute(imgL, imgR)

# Plot the results
plt.imshow(disparity, 'gray')
plt.show()

