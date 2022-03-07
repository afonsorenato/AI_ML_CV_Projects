import cv2
import numpy as np

# Variables
frameCount = 0
resize_factor = 0.25
frame_cnt_cond = 1
cnt_cond = 5000

# Printing variables
FONT = cv2.FONT_HERSHEY_SIMPLEX
COLOR = (0, 0, 255)

# Get video capture
#cap = cv2.VideoCapture("soggiorno full hd.mp4")
cap = cv2.VideoCapture(0)

# Get background subtraction
fg_bg = cv2.createBackgroundSubtractorMOG2(300, 400, True)

while True:

    # Get frame
    ret, frame = cap.read()
    frameCount += 1

    # Stop condition
    if not ret:
        break

    # Resize image
    resizedFrame = cv2.resize(frame, (0, 0), fx=resize_factor, fy=resize_factor)

    # Apply mask
    fg_mask = fg_bg.apply(resizedFrame)

    # Count number of nn zero values
    count = np.count_nonzero(fg_mask)
    print('Frame: %d, Pixel Count: %d' % (frameCount, count))

    if frameCount > frame_cnt_cond and count > cnt_cond:
        print('Persona nel soggiorno! \n')
        cv2.putText(resizedFrame, 'Persona nel soggiorno', (10, 50), FONT, 1, COLOR, 2,
                    cv2.LINE_AA)

        # File opener
        with open('minuto.txt', 'w') as f:
            f.write('secondo di motion')
            continue

    # Final plots
    cv2.namedWindow("Final Output", cv2.WINDOW_NORMAL)
    cv2.imshow('Final Output', resizedFrame)

    cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
    cv2.imshow('Mask', fg_mask)

    if cv2.waitKey(1) & 0xff == 27:
        break


cap.release()
cv2.destroyAllWindows()