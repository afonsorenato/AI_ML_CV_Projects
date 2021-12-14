import cv2
import mediapipe as mp
import time
import os
import AllMethods
import HandTrackingModule as hm


mpHands = mp.solutions.hands
hands = mpHands.Hands()  #Uses rgb image
mpDraw = mp.solutions.drawing_utils
detectorHands = hm.handDetector(detectionCon=0.7)

mpDrawPose = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
color = (0,255,0)

def getTips(myList, overlayList):
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)
    pTime = 0
    detector = hm.handDetector(detectionCon=0.70)
    tipIds = [4, 8, 12, 16, 20]

    return tipIds, detector, overlayList

def getFingers(img):
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=True)
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
        #h, w, c = overlayList[totalFingers - 1].shape
        #img[0:h, 0:w] = overlayList[totalFingers - 1]

    return totalFingers



mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
folderPath = "Fingers"
myList = os.listdir(folderPath)
overlayList = []
tipIds, detector, overlayList = getTips(myList, overlayList)


cap = cv2.VideoCapture(0)


total = 0

while True:
    suc, img = cap.read()

    aux_img = img[0:200,0:640]
    total = getFingers(aux_img)
    print(total)

    #imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #img = AllMethods.getBody(img, pose, mpPose, mpDrawPose)
    #img = AllMethods.getHands(img, detectorHands, color)

    print(aux_img.shape)
    cv2.imshow("Image", aux_img)
    cv2.waitKey(1)

