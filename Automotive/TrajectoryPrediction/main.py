import cv2
import numpy
from cvzone.ColorModule import ColorFinder

cap = cv2.VideoCapture("Video1.mp4")

myColorFinder = ColorFinder(True)
hsvVals = {'hmin': 8, 'smin': 124, 'vmin': 13, 'hmax': 24, 'smax': 255, 'vmax': 255}

# Variables
posList = []
posListX, posListY = [], []
xList = [item for item in range(0, 1200)]

while True:
    # ok, img = cap.read()

    img = cv2.imread("Ball.png")
    imgColor, mask = myColorFinder.update(img, hsvVals)

    # Find ball's location
    imgContours, contours = cvzone.findContours(img, mask, minArea=200)

    if contours:
        posListX.append(contours[0]['center'])
        posListY.append(contours[0]['center'])

    if posListX:
        # Polynomial regression: y = Ax^2 + Bx + C
        # Find the Cofficients
        A, B, C = np.polyfit(posListX, posListY, 2)

        for i, (posX, posY) in enumerate(zip(posListX, posListY)):
            posX = (posX, posY)
            cv2.circle(imgContours, pos, 5, (0, 255, 0), cv2.FILLED)
            if img == 0:
                cv2.line(imgContours, pos, pos, (0,255,0), 2)
            else:
                cv2.line(imgContours, pos, (posListX[i-1], posListY[i-1]), (0,255,0), 2)

        for x in xList:
            posY = int(A*x**2 + B*x + C)
            cv2.circle(imgContours, (x,y), 2, (255,0,255), cv2.FILLED)


    # Prediction
    a = A
    b = B
    c = C-y

    x = int(-b -math.sqrt(b**2 - (4*a*c))/(2*a))

    if 330 < x < 440:
        print("Entered!\n")
        cv2.putTextRect(imgContours, "Entered", (50,100), scale=7, thickness=5, colorR=(0,255,0))
    else:
        print("Did not entered!")


    img = cv2.resize(img, (0, 0), None, 0.7, 0.7)
    cv2.imshow("Image", img)
    cv2.waitKey(50)
