import cv2
import time
import numpy as np
import HandTrackingModule

#Variables
wCam , hCam = 640, 480


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

while True:
    ok, img = cap.read()

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (40, 40), cv2.FONT_HERSHEY_SIMPLEX,
            1, (255,0,0), 2)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
