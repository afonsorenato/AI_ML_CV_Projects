import cv2
import numpy as np
import time
import mediapipe as mp
import math

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()


cap = cv2.VideoCapture(0)

#--------------------------
def getLandmarks(img, mpDraw, mpPose, pose):

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    lmList = []

    if results.pose_landmarks:
        mpDraw.draw_landmarks(img,results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            lmList.append([id, cx, cy])
            cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)
    return img, lmList

def findAngle(img, p1, p2, p3, lmList):
    x1, y1 = lmList[p1][1:]
    x2, y2 = lmList[p2][1:]
    x3, y3 = lmList[p3][1:]

    #Angle
    aux1 = math.atan2(y3-y2,x3-x2)
    aux2 = math.atan2(y1-y2, x1-x2)
    angle = int(-math.degrees(aux1-aux2))
    cv2.putText(img, str(angle), (x2+50, y2-50),
                cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)


    cv2.line(img, (x1, y1), (x2, y2), (255,255,255), 3)
    cv2.line(img, (x3, y3), (x2, y2), (255,255,255), 3)

    cv2.circle(img, (x1, y1), 8, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x1, y1), 8, (0, 0, 255), 2)
    cv2.circle(img, (x2, y2), 8, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x2, y2), 8, (0, 0, 255), 2)
    cv2.circle(img, (x3, y3), 8, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x3, y3), 8, (0, 0, 255), 2)

    return img

#-------------------MAIN----------------------
while True:
    suc, img = cap.read()
    img, lmList = getLandmarks(img, mpDraw, mpPose, pose)

    img = findAngle(img, 12, 14, 16, lmList)



    cv2.imshow("image", img)
    cv2.waitKey(1)

