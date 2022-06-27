import cv2
import time
import numpy as np

from cam_config import *

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




    # End time
    end = time.time()
    fps = 1/(end-start)
    cv2.putText(img, f"{fps:.2f} FPS", (50, 50),
                FONT, 4, RED, 2)


    cv2.imshow("Image", img)
    #cv2.imshow("Depth Map", output)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


