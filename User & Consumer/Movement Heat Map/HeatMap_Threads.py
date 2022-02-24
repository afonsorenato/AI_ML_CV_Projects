import cv2
import copy
import numpy as np

from threading import Thread

# Variables
threshold = 2
maxValue = 2



"""
Gets the current frame and outputs the heat colored map 
Return the colored heat map and original frame
"""
def plotHeatMapUp():
    final_up = cv2.hconcat([frame, out_color], (300, 150))
    cv2.namedWindow("Frame Up", cv2.WINDOW_NORMAL)
    cv2.imshow("Frame Up", final_up)
    cv2.waitKey(1)


"""
Gets the current frame and outputs the heat colored map
Return gray scaled image 
"""
def plotHeatMapDown():
    final_bottom = cv2.hconcat([accum_image, accum_image], (300, 150))
    cv2.namedWindow("Frame Down", cv2.WINDOW_NORMAL)
    cv2.imshow("Frame Down", final_bottom)
    cv2.waitKey(1)


# Init capture
cap = cv2.VideoCapture(0)

background_sub = cv2.bgsegm.createBackgroundSubtractorMOG()
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Get frame
ok, frame = cap.read()

# Gets first frame and the original background
first_frame = copy.deepcopy(frame)
h, w = frame.shape[:2]
accum_image = np.zeros((h, w), np.uint8)

while ok:
    ok, frame = cap.read()
    filter = background_sub.apply(frame)
    ret, th1 = cv2.threshold(filter, threshold, maxValue, cv2.THRESH_BINARY)
    accum_image = cv2.add(accum_image, th1)

    out_color = cv2.applyColorMap(accum_image, cv2.COLORMAP_HOT)

    # Create threads
    t1 = Thread(target=plotHeatMapUp())
    t2 = Thread(target=plotHeatMapDown())

    # Start threads
    t1.start()
    t2.start()

    t1.join()
    t2.join()
