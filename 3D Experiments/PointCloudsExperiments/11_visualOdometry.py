import os
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt



"""
Applications:
1. Self driving cars
2. space exploration
3. mapping of environments
4. localization in environments

RGBD odometry finds the camera movement between two consecutive images.
The input are two instances of RGBD images and the output is the motion in the form of a rigid body transformation.
"""
import os
import copy
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

rgbd_data = o3d.data.SampleRedwoodRGBDImages()

source_color = o3d.io.read_image(rgbd_data.color_paths[0])
source_depth = o3d.io.read_image(rgbd_data.depth_paths[0])

target_color = o3d.io.read_image(rgbd_data.color_paths[4])
target_depth = o3d.io.read_image(rgbd_data.depth_paths[4])

source_rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(source_depth, source_depth)
source_pcd = o3d.geometry.PointCloud.create_from_rgbd_image(source_rgbd_image, pinhole_camera_intrinsic)

target_rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(target_depth, target_depth)
target_pcd = o3d.geometry.PointCloud.create_from_rgbd_image(target_rgbd_image, pinhole_camera_intrinsic)


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])

    source_temp.transformation(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])


option = o3d.pipelines.odometry.OdometryOption()
odo_init = np.identity(4)
print(option)

draw_registration_result(source_pcd, target_pcd, odo_init)
