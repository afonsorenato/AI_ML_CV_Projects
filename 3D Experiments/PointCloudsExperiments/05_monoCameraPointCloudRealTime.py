import cv2
import yaml
import torch
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from yaml.loader import SafeLoader

# Load a MiDas model for depth estimation
# Source: https://www.youtube.com/watch?v=MNzdybzH0kM&ab_channel=NicolaiNielsen-ComputerVision%26AI

# model_type = "DPT_Large"     # MiDaS v3 - Large     (highest accuracy, slowest inference speed)
# model_type = "DPT_Hybrid"   # MiDaS v3 - Hybrid    (medium accuracy, medium inference speed)
model_type = "MiDaS_small"  # MiDaS v2.1 - Small   (lowest accuracy, highest inference speed)

midas = torch.hub.load("intel-isl/MiDaS", model_type)

# Move model to GPU if available
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
midas.to(device)
midas.eval()

# Load transforms to resize and normalize the image
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
    transform = midas_transforms.dpt_transform
else:
    transform = midas_transforms.small_transform

# Open up the video capture from a webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():

    success, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Apply input transforms
    input_batch = transform(img).to(device)

    # Prediction and resize to original resolution
    with torch.no_grad():
        prediction = midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1), size=img.shape[:2], mode="bicubic", align_corners=False, ).squeeze()

    depth_map = prediction.cpu().numpy()

    depth_map = cv2.normalize(depth_map, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_64F)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    depth_map = (depth_map * 255).astype(np.uint8)
    depth_map = cv2.applyColorMap(depth_map, cv2.COLORMAP_MAGMA)

    # Get the live point-cloud
    cv2.imwrite("color_raw.jpg", img)
    cv2.imwrite("depth_raw.png", depth_map)

    # Reads the images using the o3d library method
    color_raw = o3d.io.read_image("color_raw.jpg")
    depth_raw = o3d.io.read_image("depth_raw.png")

    # Creates the RGDB image
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw)
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image,
                                                         o3d.camera.PinholeCameraIntrinsic(
                                                             o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0],
                   [0, 0, 1, 0], [0, 0, 0, 1]])
    o3d.visualization.draw_geometries([pcd])
    # cv2.imshow('Image', img)
    # cv2.imshow('Depth Map', depth_map)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
