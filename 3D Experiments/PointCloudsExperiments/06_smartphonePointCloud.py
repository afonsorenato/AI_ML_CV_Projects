import cv2
import yaml
import torch
import imutils
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

"""
ICP means iterative closest point registration algorithm: the input are two
point clouds and an initial tranformation that align with the source point
cloud to the target point cloud.

The output is a refined transformation that alights the two point clouds.
"""

images = [cv2.imread("Samples_PointClouds/Room_Reconstruct/00001.tiff"),
          cv2.imread("Samples_PointClouds/Room_Reconstruct/00020.tiff")]


stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)

print(status)
print(stitched)

cv2.namedWindow("Results", cv2.WINDOW_NORMAL)
cv2.imshow("Results", stitched)
cv2.waitKey(0)