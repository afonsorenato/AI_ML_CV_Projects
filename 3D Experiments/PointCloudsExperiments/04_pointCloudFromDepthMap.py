import os
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

print("Read Redwood dataset.\n")

color_raw = o3d.io.read_image("Samples_PointClouds/00002.jpg")
depth_raw = o3d.io.read_image("Samples_PointClouds/00002.png")

rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw)
print(rgbd_image)

plt.subplot(1, 2, 1)
plt.title("Gray scale image")
plt.imshow(rgbd_image.color)
plt.subplot(1, 2, 2)
plt.title("Gray depth image")
plt.imshow(rgbd_image.depth)
plt.show()

pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image,
                                                     o3d.camera.PinholeCameraIntrinsic(
                                                         o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
o3d.visualization.draw_geometries([pcd])

"""
It is used the pinhole camera model as default parameters. It assumes
fl = (525, 525) and c = (319, 319). The extrisic are assumed as the identity
matrix.
"""
