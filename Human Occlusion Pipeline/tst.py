import cv2

cap = cv2.VideoCapture('CleanVideo1.mp4')
ok, frame = cap.read()

while ok:
    ok, frame = cap.read()
    cv2.imshow("OUt", frame)
    cv2.waitKey(1)