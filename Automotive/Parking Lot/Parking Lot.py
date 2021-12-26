import cv2
import pickle

w, h = 55, 30
posList = []

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def mouseClick(events, x, y, flag, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + w and y1 < y < y1 + h:
                posList.pop(i)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread("Others/carParkingImg.png")

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + w, pos[1] + h), (255, 0, 255), 2)

    cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
    cv2.imshow("Output", img)
    cv2.setMouseCallback("Output", mouseClick)
    cv2.waitKey(1)
