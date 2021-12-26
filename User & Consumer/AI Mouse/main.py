import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

# Variables
wCam = 640
hCam = 480
frameR = 100
pTime = 0
smoothening = 10

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
wScr, hScr = autopy.screen.size()

plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Detector initialization
detector = htm.handDetector(maxHands=1)

while True:
    ok, img = cap.read()
    img = detector.findHands(img)

    # Find hand landmarks
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (255,0,255), 2)


        # Get tip of the index finger: Moving mode
        if fingers[1] == 1 and fingers[2] == 0:

            # Convert coordinates and Smooth this values
            x3 = np.interp(x1, (frameR, wCam-frameR), (0,wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0,hScr))

            # Smooth the values
            clocX = plocX + (x3 - plocX / smoothening)
            clocY = plocY + (x3 - plocY / smoothening)

            # Move mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1,y1), 5, (255,0,255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # Middle and index are up: clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 5, (0,255,0), -1)
                autopy.mouse.click()


    # Frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20,60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
