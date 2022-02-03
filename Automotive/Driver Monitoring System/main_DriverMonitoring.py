import dmsLib
import numpy as np
import cv2, pickle, os, dlib, time
from Aux_Files import DriverID

cap = cv2.VideoCapture(0)
net, predictor_path, predictor, detector = dmsLib.getModelsParameters()
count, reshape_factor = 0, 0.4
frame_size = (860, 860)

# Define the codec for video saving
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv2.VideoWriter("DMS_demo.avi", fourcc, 10.0, frame_size)

while True:
    # Get frame from webcam
    ok, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ok:
        break

    # Outputs if the eyes are closed on not
    frame, count = dmsLib.getEyeClose(frame, predictor_path, predictor, detector, count)

    # Detects if there is a phone on scene
    frame, color = dmsLib.getCellPhone(frame, net, dmsLib.getClasses(), (0, 255, 0))
    frame = cv2.resize(frame, frame_size)

    # Display
    cv2.namedWindow("Driver Monitoring", cv2.WINDOW_NORMAL)
    cv2.imshow('Driver Monitoring', frame)

    # Save video
    out.write(frame)

cap.release()
out.release()
cv2.destroyAllWindows()
