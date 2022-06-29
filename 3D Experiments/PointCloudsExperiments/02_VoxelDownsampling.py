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

"""
Voxel: group of 3D points that is used to down-sample a Point-cloud.
Points are bucketed into voxels (groups, buckets).
Each occupied voxel generates exatly one point by averaging all points inside
"""
print("Loading point-cloud, print and render it:")

# Reads the point-cloud
pcd = o3d.io.read_point_cloud("Samples_PointClouds/fragment.ply")
print(pcd)
#print(np.asarray(pcd.points))

# Visualizes the point-cloud using mouse
o3d.visualization.draw_geometries([pcd],
                                  zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])

# Voxel down-sampling
print("\nNow, let's down-sample the point-cloud with a voxel of 0.05")
downpcd = pcd.voxel_down_sample(voxel_size = 0.05)

print(downpcd)
#print(np.asarray(downpcd.points))
o3d.visualization.draw_geometries([downpcd],
                                  zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])

# Other basic operation for point-clouds is Point normal estimation.
# Computes the normal for every points: finds adjacent points and calculates
# the principal axis of the adjacent points using covariance analysis.
# Its the normal vector of the points according to the plane.
# Press N to see point normals and +, - to control the length of the normal
print("\nRecompute the normal of the down-sampled points.")

downpcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
o3d.visualization.draw_geometries([downpcd],
                                  zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024],
                                  point_show_normal=True)

# Access estimated vertex normal
print("\nPrint a normal vector of the 0th point.")
print(downpcd.normals[0])

print("\nPrint a normal vector of the first 10 points.")
print(np.asarray(downpcd.normals)[:10, :])


