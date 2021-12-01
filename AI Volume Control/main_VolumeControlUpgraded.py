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
area = 0
vol = volBar = volPer = 0

#Detector
detector = htm.handDetector(detectionCon = 0.7)

while True:
    ok, img = cap.read()
    # Find hand
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, 0, draw=True)

    if len(lmList) != 0:

        # Filter based on size
        if bbox != []:
            area = abs((bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100)+ 1
        else:
            area = 0

        if 250 < area < 1000:
            # Find distance between index and thumb
            length, img, lineInfo = detector.findDistance(4, 8, img, True)
            print("Length: " + str(length))

            vol = np.interp(length, [50, 300], [minVol, maxVol])
            volBar = np.interp(length, [50, 300], [400, 150])
            volPer = np.interp(length, [50, 300], [0, 100])
            cv2.putText(img,  str(int(volPer)), (50, 435), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

            volume.SetMasterVolumeLevel(0, None)
            cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), -1)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    cv2.imshow("Img", img)
    cv2.waitKey(1)

volume.SetMasterVolumeLevel(0, None)

