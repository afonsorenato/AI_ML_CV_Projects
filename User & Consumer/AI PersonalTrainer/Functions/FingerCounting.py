import cv2
import time
import os
import HandTrackingModule as hm


folderPath = "Fingers"
myList = os.listdir(folderPath)
overlayList = []

def getTips(myList, overlayList):
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)
    pTime = 0
    detector = hm.handDetector(detectionCon=0.75)
    tipIds = [4, 8, 12, 16, 20]

    return tipIds, detector, overlayList

def getFingers(img):
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []
        # Thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(0)
        else:
            fingers.append(1)

        # Other fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)
        h, w, c = overlayList[totalFingers - 1].shape
        img[0:h, 0:w] = overlayList[totalFingers - 1]

    return img

#-----------------------------------

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

tipIds, detector, overlayList = getTips(myList, overlayList)

while True:
    suc, img = cap.read()
    img = getFingers(img)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


