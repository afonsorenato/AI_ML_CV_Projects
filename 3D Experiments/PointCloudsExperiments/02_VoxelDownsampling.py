"""
*********** Renato Afonso - 2022 ***********
Some revisions / recalling some 3D vision concepts
"""

import matplotlib.pyplot as plt
import open3d as o3d
import numpy as np
import copy
import sys
import os

# Voxel: group of 3D points that is used to down-sample a PC
print("Loading point-cloud, print and render it:")

# Reads the point-cloud
pcd = o3d.io.read_point_cloud("Samples_PointClouds/fragment.ply")
print(pcd)
print(np.asarray(pcd.points))

# Visualizes the point-cloud using mouse
o3d.visualization.draw_geometries([pcd],
                                  zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])

# Voxel down-sampling
print("Now, let's down-sample the point-cloud with a voxel of 0.05")
downpcd = pcd.voxel_down_sample(voxel_size = 0.05)

o3d.visualization.draw_geometries([downpcd],
                                  zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])