import cv2, time, os
from Intruder_module import getPrediction, enterPassword, sendEmail

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("C:/Users/Renato/OneDrive/Ambiente de Trabalho/intruder_video.mp4")
directory = "../House Intruder"

# Gets first frame
ok, frame = cap.read()
email_sent = False

# Asks email password for intruder warning
password = enterPassword()
init = time.time()

while ok:
    # Get frame
    ok, frame = cap.read()
    if not ok:
        print("Program terminated.\n")
        break

    # Human detection
    prediction, human_detected = getPrediction(frame)

    if human_detected and email_sent is False:
        sendEmail(password, frame)
        email_sent = True

    # Plot the obtained image
    cv2.namedWindow("Live stream", cv2.WINDOW_NORMAL)
    cv2.imshow("Live stream", frame)
    cv2.waitKey(1)

    # Update warning rate
    elapsed_time = int(time.time() - init)
    if elapsed_time > 60:
        email_sent = False
        init = time.time()

#cleanImages(directory)
