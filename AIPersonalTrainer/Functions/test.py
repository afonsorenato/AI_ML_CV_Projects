import cv2
import numpy as np
import time
import mediapipe as mp
import HandTrackingModule as hm
import math
import os
import trainMenu

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
folderPath = "Fingers"
myList = os.listdir(folderPath)
overlayList = []

def getTips(myList, overlayList):
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)
    pTime = 0
    detector = hm.handDetector(detectionCon=0.70)
    tipIds = [4, 8, 12, 16, 20]

    return tipIds, detector, overlayList


cap = cv2.VideoCapture(0)
tipIds, detector, overlayList = getTips(myList, overlayList)



while True:
    suc, img  = cap.read()
    lmList = detector.findPosition(img, draw=True)
    img = detector.findHands(img)
    totalFingers = 0

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
        cv2.imshow("img", img)
        cv2.waitKey(1)