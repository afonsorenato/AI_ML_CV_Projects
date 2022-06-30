import matplotlib.pyplot as plt
import open3d as o3d
import numpy as np
import os

path_point_cloud = "Samples_PointClouds/fragment.ply"
path_chair_crop = "Samples_PointClouds/cropped.json"


# Visualize point cloud
def visualizePointCloud(path_point_cloud):
    pcd = o3d.io.read_point_cloud(path_point_cloud)
    o3d.visualization.draw_geometries([pcd],
                                      zoom=0.3412,
                                      front=[0.4257, -0.2125, -0.8795],
                                      lookat=[2.6172, 2.0475, 1.532],
                                      up=[-0.0694, -0.9768, 0.2024])


# Crop point cloud
def cropPointCloud(path_point_cloud):
    """
    Reads a json file that specifies a polygon selection area
    """
    print("\nReturns the cropped 3D chair of this scene.")
    pcd = o3d.io.read_point_cloud(path_point_cloud)
    vol = o3d.visualization.read_selection_polygon_volume(path_chair_crop)
    chair = vol.crop_point_cloud(pcd)
    o3d.visualization.draw_geometries([chair],
                                      zoom=0.7, front=[0.5439, -0.2333, -0.8060],
                                      lookat=[2.4615, 2.1331, 1.338], up=[-0.1781, 0.9708, 0.1608])


# Paint point cloud
def paintCroppedObjectInPointCloud(path_point_cloud, path_chair_crop):
    pcd = o3d.io.read_point_cloud(path_point_cloud)
    vol = o3d.visualization.read_selection_polygon_volume(path_chair_crop)
    chair = vol.crop_point_cloud(pcd)

    print("\nPainted chair.")
    chair.paint_uniform_color([0, 0, 1])  # RGB [0-1]
    o3d.visualization.draw_geometries([chair],
                                      zoom=0.7, front=[0.5439, -0.2333, -0.8060],
                                      lookat=[2.4615, 2.1331, 1.338], up=[-0.1781, 0.9708, 0.1608])


# Point cloud distance
def computePointCloudDistances(path_point_cloud, path_chair_crop):
    pcd = o3d.io.read_point_cloud(path_point_cloud)
    vol = o3d.visualization.read_selection_polygon_volume(path_chair_crop)
    chair = vol.crop_point_cloud(pcd)

    print("\nCompute the distance between two points on the point-cloud.")

    dists = pcd.compute_point_cloud_distance(chair)
    dists = np.asarray(dists)

    ind = np.where(dists > 0.01)[0]
    pcd_without_chair = pcd.select_by_index(ind)
    o3d.visualization.draw_geometries([pcd_without_chair],
                                      zoom=0.3412,
                                      front=[0.4257, -0.2125, -0.8795],
                                      lookat=[2.6172, 2.0475, 1.532],
                                      up=[0.0694, -0.9768, 0.2024])


# Bounding volumes
def boundingVolumesInPointCloud(path_point_cloud, path_chair_crop):
    """
    The point cloud geometry type has bounding boxes as all other geometry in open3D.
    It implements an aligned or oriented bounding box that can also be used to crop the geometry
    """

    # Crops the 3D point cloud with the chair
    pcd = o3d.io.read_point_cloud(path_point_cloud)
    vol = o3d.visualization.read_selection_polygon_volume(path_chair_crop)
    chair = vol.crop_point_cloud(pcd)

    aabb = chair.get_axis_aligned_bounding_box()
    aabb.color = (1, 0, 0)
    obb = chair.get_oriented_bounding_box()
    obb.color = (0, 1, 0)

    o3d.visualization.draw_geometries([chair, aabb, obb],
                                      zoom=0.7, front=[0.5439, -0.2333, -0.8060],
                                      lookat=[2.4615, 2.1331, 1.338], up=[-0.1781, 0.9708, 0.1608])


# Context plot
def boundingVolumesInPointCloud(path_point_cloud):
    # Crops the 3D point cloud with the chair
    pcd = o3d.io.read_point_cloud(path_point_cloud)

    with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
        labels = np.array(pcd.cluster_dbscan(eps=0.02, min_points=10, print_progress=True))

    max_label = labels.max()
    print(f"Point cloud has {max_label + 1} clusters.")
    colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])

    o3d.visualization.draw_geometries([pcd],
                                      zoom=0.455,
                                      front=[0.4999, -0.1659, -0.8499],
                                      lookat=[2.1813, 2.0619, 2.0999],
                                      up=[-0.1204, 0.9852, 0.1215])


# visualizePointCloud(path_point_cloud)
# cropPointCloud(path_point_cloud)
# paintCroppedObjectInPointCloud(path_point_cloud, path_chair_crop)
# computePointCloudDistances(path_point_cloud, path_chair_crop)
boundingVolumesInPointCloud(path_point_cloud)
