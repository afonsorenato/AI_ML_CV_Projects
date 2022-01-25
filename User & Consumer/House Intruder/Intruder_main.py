import cv2
import time
from Intruder_module import getPrediction, sendEmail, enterPassword, sendImageEmail

# Get video from webcam
# Detect human
# Send email

cap = cv2.VideoCapture(0)
ok, frame = cap.read()

# Asks email password for intruder warning
password = enterPassword()


while ok:
    # Get frame
    ok, frame = cap.read()

    # Human detection
    prediction, human_detected = getPrediction(frame)

    if human_detected:
        saved_image = cv2.imwrite("IntruderSnapShot.jpg", frame)
        sendEmail(password)
        #sendImageEmail()
        time.sleep(60)

    cv2.namedWindow("Live stream", cv2.WINDOW_NORMAL)
    cv2.imshow("Live stream", frame)
    cv2.waitKey(1)