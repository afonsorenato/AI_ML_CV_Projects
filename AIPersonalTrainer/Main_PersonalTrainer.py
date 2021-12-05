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
            #cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)
    return img, lmList
def findAngle(img, p1, p2, p3, lmList):

    x1, y1 = lmList[p1][1:]
    x2, y2 = lmList[p2][1:]
    x3, y3 = lmList[p3][1:]

    #Angle
    aux1 = math.atan2(y3-y2,x3-x2)
    aux2 = math.atan2(y1-y2, x1-x2)
    angle = int(math.degrees(aux1-aux2))
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

    return img, abs(angle)

def getSquat(img, lmList, prev_pos, actual_pos, count):

    img, ang_left = findAngle(img, 23, 25, 27, lmList)
    ang_left = abs(ang_left)
    img, ang_right = findAngle(img, 24, 26, 28, lmList)
    ang_right = abs(ang_right)

    prev_pos = actual_pos

    if (ang_left > 90 and ang_left < 220) and (ang_right > 90 and ang_right < 220):
        #print("Up")
        actual_pos = 0
    if (ang_left > 200) or (ang_right < 150):
        #print("Squat")
        actual_pos = 1


    if prev_pos == 1 and actual_pos==0:
        print("One more!")
        count = count + 1

    cv2.putText(img, str(count), (300, 80), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 3)
    return img, prev_pos, actual_pos, count

def getLegRaises(img, lmList, prev_pos, actual_pos, count):

    img, ang_left = findAngle(img, 11, 23, 25, lmList)
    ang_left = abs(ang_left)
    img, ang_right = findAngle(img, 12, 24, 26, lmList)
    ang_right = abs(ang_right)

    prev_pos = actual_pos

    if ang_left < 120 or ang_right < 120:
        #print("Up")
        actual_pos = 0
    else:
        #print("Squat")
        actual_pos = 1

    if prev_pos == 1 and actual_pos==0:
        print("One more!")
        count = count + 1

    cv2.putText(img, str(count), (300, 80), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 3)
    return img, prev_pos, actual_pos, count

def getTips(myList, overlayList):
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)
    pTime = 0
    detector = hm.handDetector(detectionCon=0.70)
    tipIds = [4, 8, 12, 16, 20]

    return tipIds, detector, overlayList


def getFingers(img):
    aux_img = img[0:250, 0:640]
    aux_img = detector.findHands(aux_img)
    lmList = detector.findPosition(aux_img, draw=True)
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

#-------------------Variables----------------------
count = 0
cnt_push = 0
cnt_leg = 0
prev_pos = 0
actual_pos = 0
count_end = 0

min_to_enter = 80
accept_squats = 0
accept_legs = 0
accept_push = 0

finger = 0
last_finger = 0
end_squat = 0
end_raises = 0
end_push = 0
lim_to_end = 40
font = cv2.FONT_HERSHEY_PLAIN
green = (0,255,0)
red = (0,0,255)

#-----------------------------------MAIN------------------------------
cap = cv2.VideoCapture(0)
tipIds, detector, overlayList = getTips(myList, overlayList)

while True:
    suc, img = cap.read()
    img = trainMenu.WelcomeMenu(img)
    last_finger = finger
    finger = getFingers(img)

    #Finish workout
    if finger == 5 and last_finger== 5:
        count_end = count_end+1
        print("Count-end:", count_end)
        if count_end >= 75:
            print("Finish your workout")
            count_end = 0
            cv2.waitKey(3000)
            break
    else:
        count_end = 0

#Exercice 1: squats------------------------------------------------------------------
    if finger == 1 and last_finger== 1:
        accept_squats = accept_squats + 1
        accept_push = 0
        accept_legs = 0
        print("accept squats: ", accept_squats)

        if accept_squats >= min_to_enter:
            accept_squats = 0
            while True:
                last_finger = finger
                suc, img = cap.read()
                finger = getFingers(img)

                if finger == 5 and last_finger == 5:
                    end_squat = end_squat + 1
                    cv2.putText(img, "Finishing exercice", (10, 70), font, 2, green, 2)
                    cv2.imshow("image", img)
                    cv2.waitKey(1)

                    print("End-squat:", end_squat)
                    if end_squat >= lim_to_end:
                        suc, img = cap.read()
                        aux = "Total squats: "+ str(count)
                        cv2.putText(img, aux, (100, 100), font, 3,  red, 3)
                        cv2.putText(img, "End of Squats", (100, 140), font, 3, red, 3)
                        cv2.imshow("image", img)
                        cv2.waitKey(4000)
                        end_squat = 0
                        break
                else:
                    aux = "Doing squats"
                    img, List = getLandmarks(img, mpDraw, mpPose, pose)
                    img, prev_pos, actual_pos, count = getSquat(img, List, prev_pos, actual_pos, count)
                    cv2.putText(img, aux, (10, 70), font ,2, green, 2)
                    cv2.imshow("image", img)
                    cv2.waitKey(1)
                    end_squat = 0

#Exercice 2: leg raises------------------------------------------------------------------
    if finger == 2 and last_finger == 2:
        accept_squats = 0
        accept_push = 0
        accept_legs = accept_legs + 1
        print("accept legs: ", accept_legs)

        if accept_legs >= min_to_enter:
            print("Entrei nos leg-raising")
            accept_legs = 0
            while True:
                last_finger = finger
                suc, img = cap.read()
                finger = getFingers(img)

                if finger == 5 and last_finger == 5:
                    end_raises = end_raises + 1
                    cv2.putText(img, "Finishing exercice", (10, 70), font, 2, green, 2)
                    cv2.imshow("image", img)
                    cv2.waitKey(1)

                    print("End-let raise:", end_raises)
                    if end_raises >= lim_to_end:
                        aux = "Total leg-raises: "+ str(cnt_leg)
                        cv2.putText(img, aux, (100, 140), font, 3, red, 3)
                        cv2.putText(img, "End of Leg-raises", (100, 100), font, 3, red, 3)
                        cv2.imshow("image", img)
                        cv2.waitKey(4000)
                        end_raises = 0
                        break
                else:
                    aux = "Doing let raises"
                    img, List = getLandmarks(img, mpDraw, mpPose, pose)
                    img, prev_pos, actual_pos, cnt_leg = getLegRaises(img, List, prev_pos, actual_pos, cnt_leg)
                    cv2.putText(img, aux, (10, 70), font, 2, green, 2)
                    cv2.imshow("image", img)
                    cv2.waitKey(1)
                    end_raises = 0

# Exercice 3: push-ups------------------------------------------------------------------
    if finger == 3 and last_finger == 3:
        accept_push = accept_push + 1
        accept_legs = 0
        accept_squats = 0
        print("accept push ups: ", accept_push)

        if accept_push >= min_to_enter:
            print("Entrei nas push-ups")
            accept_push = 0
            while True:
                    last_finger = finger
                    suc, img = cap.read()
                    finger = getFingers(img)

                    if finger == 5 and last_finger == 5:
                        cv2.putText(img, "Finishing exercice", (10, 70), font, 2, green, 2)
                        cv2.imshow("image", img)
                        end_push = end_push + 1
                        cv2.waitKey(1)

                        print("End push-ups:", end_push)
                        if end_push >= lim_to_end:
                            aux = "Total push-ups: "+ str(cnt_push)
                            cv2.putText(img, aux, (100, 140), font, 3, (0, 0, 255), 3)
                            cv2.putText(img, "End of push-ups", (100, 100), font, 3, red, 3)
                            cv2.imshow("image", img)
                            cv2.waitKey(4000)
                            end_push = 0
                            break
                    else:
                        aux = "Doing push-ups"
                        img, List = getLandmarks(img, mpDraw, mpPose, pose)
                        img, prev_pos, actual_pos, cnt_push = getLegRaises(img, List, prev_pos, actual_pos, cnt_push)
                        cv2.putText(img, aux, (10, 70), font, 2, green, 2)
                        cv2.imshow("image", img)
                        cv2.waitKey(1)
                        end_push = 0

    #Keeps waiting for order
    else:
        cv2.imshow("image", img)
        cv2.waitKey(1)

print("Good workout\n")
