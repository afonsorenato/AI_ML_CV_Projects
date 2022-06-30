import cv2
import yaml
import torch
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

"""
ICP means iterative closest point registration algorithm: the input are two
point clouds and an initial tranformation that align with the source point
cloud to the target point cloud.

The output is a refined transformation that alights the two point clouds.
"""