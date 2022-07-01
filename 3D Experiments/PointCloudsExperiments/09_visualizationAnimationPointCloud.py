import cv2
import yaml
import torch
import imutils
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt


if __name__ == "__main__":

    pcd = o3d.io.read_point_cloud("Samples_PointClouds/my_room2.ply")
    o3d.visualization.draw_geometries([pcd])

