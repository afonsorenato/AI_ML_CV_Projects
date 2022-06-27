import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

from cam_config import *
from mpl_toolkits.mplot3d import Axes3D

# Path where the model is
path_model = "Models/"

# Read network
model_name = "model-f6b98070.onnx"  # large model
# model_name = "model-small.onnx"  # small model

# Load the Dnn model
model = cv2.dnn.readNet(path_model + model_name)

if model.empty():
    print("Could not load|!\n")

# Webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():

    ok, img = cap.read()
    imgH, imgW, chan = img.shape

    # Fps
    start = time.time()

    # Create blob from input image
    blob = cv2.dnn.blobFromImage(img, 1 / 255., (384, 384), (123.675, 116.28, 103.53), True, False)

    # Set input to the model
    model.setInput(blob)

    # Make forward pass in model
    output = model.forward()
    output = output[0, :, :]
    output = cv2.resize(output, (imgW, imgH))

    # Normalize the output
    output = cv2.normalize(output, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    # End time
    end = time.time()
    fps = 1 / (end - start)
    cv2.putText(img, f"{fps:.2f} FPS", (50, 50), FONT, 1, RED, lINE_THICKNESS)

    cv2.imshow("Image", img)
    cv2.imshow("Depth Map", output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('./Results/depth_map1.png', output*255)
        break

