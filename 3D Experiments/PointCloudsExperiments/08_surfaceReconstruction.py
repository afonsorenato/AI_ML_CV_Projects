import cv2
import yaml
import torch
import imutils
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

"""
Surface reconstruction: the first step gets us an unstructured point-cloud. To get a triangle
mesh from this unstructred input, we need to perform surface reconstruction.
Some existing methods are:
1. Alpha shapes (triangle meshes)
2. Ball pivoting
3. Poisson surface reconstruction
"""

pcd = o3d.io.read_point_cloud("Samples_PointClouds/my_room2.ply")
o3d.visualization.draw_geometries([pcd])

# Creates a mesh from a point-cloud
with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as cm:
    mesh, densities = \
        o3d.geometry.\
            TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)

print(mesh)
o3d.visualization.draw_geometries([mesh],
                                  zoom=0.664,
                                  front=[-0.4761, -0.4698, -0.7434],
                                  lookat=[1.8900, 3.2596, 0.9284],
                                  up=[0.2304, -0.8825, 0.4101])



