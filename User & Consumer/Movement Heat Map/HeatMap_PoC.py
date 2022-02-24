import cv2
import copy
import numpy as np


# Init capture
cap = cv2.VideoCapture(0)

background_sub = cv2.bgsegm.createBackgroundSubtractorMOG()
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# First frame
ok, frame = cap.read()

# Variables
threshold = 2
maxValue = 2

# Gets frist frame and the original background
first_frame = copy.deepcopy(frame)
h, w = frame.shape[:2]
accum_image = np.zeros((h, w), np.uint8)

while True:
    ok, out_original = cap.read()

    filter = background_sub.apply(out_original)
    ret, th1 = cv2.threshold(filter, threshold, maxValue, cv2.THRESH_BINARY)
    accum_image = cv2.add(accum_image, th1)

    out_color = cv2.applyColorMap(accum_image, cv2.COLORMAP_HOT)

    final_up = cv2.hconcat([out_original, out_color], (300, 150))
    final_bottom = cv2.hconcat([accum_image, accum_image], (300, 150))

    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.imshow("Frame", final_up)
    cv2.waitKey(1)
