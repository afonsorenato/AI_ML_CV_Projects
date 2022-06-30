
"""
*********** Renato Afonso - 2022 ***********
Some revisions / recalling some 3D vision concepts
"""

import open3d as o3d
import numpy as np
import sys
import os


# Reads the ply point-cloud file
# This one as 173000 points to draw the 3D object
#pcd = o3d.io.read_point_cloud("Samples_PointClouds/armadillo.ply")
#pcd = o3d.io.read_point_cloud("Samples_PointClouds/fragment.ply")
pcd = o3d.io.read_point_cloud("Samples_PointClouds/my_room2.ply")


print(pcd)
print(np.asarray(pcd.points))
o3d.visualization.draw_geometries([pcd])
