import cv2
import numpy as np
import dlib

def norma(a, b):
    c = a[0] - b[0]
    d = a[1] - b[1]
    y = (c, d)
    return np.sqrt(y[0] * y[0] + y[1] * y[1])

def getEAR(landmarks):
    #Get EAR - ||p2-p6|| + ||p3-p5||)/(2*||p1-p4||
    p1 = (landmarks.part(36).x, landmarks.part(36).y)
    p2 = (landmarks.part(37).x, landmarks.part(37).y)
    p3 = (landmarks.part(38).x, landmarks.part(38).y)
    p4 = (landmarks.part(39).x, landmarks.part(39).y)
    p5 = (landmarks.part(40).x, landmarks.part(40).y)
    p6 =(landmarks.part(41).x, landmarks.part(41).y)
    EAR_right = (norma(p2, p6) + norma(p3,p5))/(2*(norma(p1, p4)))

    p1 = (landmarks.part(42).x, landmarks.part(42).y)
    p2 = (landmarks.part(43).x, landmarks.part(43).y)
    p3 = (landmarks.part(44).x, landmarks.part(44).y)
    p4 = (landmarks.part(45).x, landmarks.part(45).y)
    p5 = (landmarks.part(46).x, landmarks.part(46).y)
    p6 =(landmarks.part(47).x, landmarks.part(47).y)
    EAR_left = (norma(p2, p6) + norma(p3,p5))/(2*(norma(p1, p4)))

    return (EAR_left + EAR_right)/2
def getInfo(landmarks, frame):
    #for i in range(0, 68):
        #cv2.circle(frame, (landmarks.part(i).x,landmarks.part(i).y), 1, (255, 0, 0), -1)

    EAR = getEAR(landmarks)
    if EAR > 0.2:
        cv2.putText(frame, "Eye's open", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, "Blinking", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    return frame

def getGaze(landmarks, frame):
    left_eye_region = np.array([
        (landmarks.part(36).x, landmarks.part(36).y),
        (landmarks.part(37).x, landmarks.part(37).y),
        (landmarks.part(38).x, landmarks.part(38).y),
        (landmarks.part(39).x, landmarks.part(39).y),
        (landmarks.part(40).x, landmarks.part(40).y),
        (landmarks.part(41).x, landmarks.part(41).y)], np.int32)

    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    left_eye = cv2.bitwise_and(gray, gray, mask=mask)

    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    gray_eye = left_eye[min_y:max_y, min_x:max_x]
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0:height, 0:int(width/2)]
    left_side_withe = cv2.countNonZero(left_side_threshold)

    right_side_threshold = threshold_eye[0:height, int(width/2):width]
    right_side_withe = cv2.countNonZero(right_side_threshold)
    gaze_ratio = left_side_withe/right_side_withe

    #eye = cv2.resize(gray_eye, None, fx=8, fy = 8)

    return right_side_threshold

#---------------------------MAIN---------------------------
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

while True:
    suc, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        frame = getInfo(landmarks, frame)
        eye = getGaze(landmarks, frame)

    cv2.imshow("Frame", eye)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
