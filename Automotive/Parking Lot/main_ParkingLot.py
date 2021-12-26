import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture("Others/parking_video.mp4")
w, h = 55, 30

# Load the file with parking lot base positions
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def checkParkingSpace(imgPro):
    for pos in posList:
        x, y = pos

        img_crop = imgPro[y:y+h, x:x+w]
        count = cv2.countNonZero(img_crop)
        #cvzone.putTextRect(img, str(count), (x, y+h-10), scale = 0.6)

        if count < 350:
            color = (0,0,255)
            thick = 2
        else:
            color = (0,255,0)
            thick = 5
        cv2.rectangle(img, pos, (pos[0] + w, pos[1] + h), color, thick)


# Main loop **************************************************
while True:
    ok, img = cap.read()

    if not ok:
        break

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAME, 0)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)

    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3,3), np.uint8)
    imDialate = cv2.dilate(imgMedian, kernel, iterations = 1)

    checkParkingSpace(imDialate)


    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", img)
    cv2.waitKey(10)