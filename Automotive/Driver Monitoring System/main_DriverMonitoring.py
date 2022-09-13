import cv2
import time
import numpy as np

from config import *
from dmsLib import *
from Aux_Files import DriverID

# Get video streaming from Webcam
cap = cv2.VideoCapture(0)

while True:

    # Get frame from webcam
    ok, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ok:
        break

    # Outputs if the eyes are closed on not
    frame, count = dmsLib.getEyeClose(frame, predictor_path, predictor, detector, count)

    # Detects if there is a phone on scene
    frame, color = dmsLib.getCellPhone(frame, net, dmsLib.getClasses(), GREEN)
    frame = cv2.resize(frame, frame_size)

    # Display
    cv2.namedWindow("Driver Monitoring", cv2.WINDOW_NORMAL)
    cv2.imshow('Driver Monitoring', frame)

    # Save video
    #out.write(frame)

cap.release()
out.release()
cv2.destroyAllWindows()
