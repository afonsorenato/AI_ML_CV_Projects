import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Volume variation required code
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-5, None)
minVol = volRange[0]
maxVol = volRange[1]

#Variables
wCam , hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
vol = volBar = volPer = 0

#Detector
detector = htm.handDetector(detectionCon = 0.7, maxHands=1)

while True:
    ok, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        P1 = lmList[4][1], lmList[4][2]
        P2 = lmList[8][1], lmList[8][2]
        P3 = (P1[0]+P2[0])//2, (P1[1]+P2[1])//2

        cv2.circle(img, P1, 15, (255,0,255), -1)
        cv2.circle(img, P2, 15, (255, 0, 255), -1)
        cv2.circle(img, P3, 15, (255, 0, 255), -1)
        cv2.line(img, P1, P2, (255,0,255), 3)

        length = math.hypot(P2[0]-P1[0], P2[1]-P1[1])
        #Hand range: 50-300
        #Volume Range: -65 - 0
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])

        volume.SetMasterVolumeLevel(vol, None)
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), -1)

        if length < 50:
            cv2.circle(img, P3, 15, (0, 255, 0), -1)

    cTime = time.time()
    fps = 1/(cTime+0.1-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    cv2.imshow("Img", img)
    cv2.waitKey(1)

volume.SetMasterVolumeLevel(0, None)

