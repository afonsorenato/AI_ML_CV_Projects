
import cv2
import dlib
import dmsLib
import numpy as np

net, predictor_path, predictor, detector = dmsLib.getModelsParameters()
count, reshape_factor = 0, 0.4
frame_size = (860, 860)

# Define the codec for video saving
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv2.VideoWriter("DMS_demo.avi", fourcc, 10.0, frame_size)