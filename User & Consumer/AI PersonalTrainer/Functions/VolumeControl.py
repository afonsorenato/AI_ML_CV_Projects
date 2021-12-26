import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.7)
count = 0
color = (0,0,255)
vol, volBar, volPer = 0,0, 0

while True:
    suc, img = cap.read()
    start = time.time()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1,y1), 5, color, cv2.FILLED)
        cv2.circle(img, (x2,y2), 5, color, cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
        cv2.circle(img, (cx,cy), 5, color, cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        #Volume range: 0:100

        vol = round(np.interp(length, [50, 250], [0, 100]), 1)
        volBar = round(np.interp(length, [50, 250], [400, 150]), 1)
        volPer = round(np.interp(length, [50, 250], [0, 100]), 1)
        print(vol)

    cv2.rectangle(img, (50, 150), (85,400), (0,255,0),3)
    cv2.rectangle(img, (50, int(volBar)), (85,400), (0,255,0),cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40,450), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0,250,0), 3)
    end = time.time()
    count = count + 1
    if count == 10:
        print("Elapsed time:", str(round(end-start, 2)))
        count = 0

    cv2.imshow("Image", img)
    cv2.waitKey(1)
