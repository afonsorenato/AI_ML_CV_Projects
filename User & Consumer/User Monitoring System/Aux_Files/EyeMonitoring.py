from playsound import playsound
import os
import dlib
import numpy as np
import cv2

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

    return (EAR_left + EAR_right)


def getEyeClose(frame, predictor_path, predictor, detector):
    cap = cv2.VideoCapture(0)
    count = 0
    SleepAlertTime = 2 #After two seconds eye close: Warning drowsiness
    faces = detector(frame)

    if faces:
        landmarks = predictor(frame, faces[0])
        for i in range(0,68):
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

        EAR_avg = getEAR(landmarks)
        if EAR_avg > 0.4:
            cv2.putText(frame, "Eye's open", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            count = 0
        else:
            cv2.putText(frame, "Eye's closed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            count = count + 1

            if count >= SleepAlertTime*30: #Assumed almost 2 seconds
                playsound('DrowsyWarning.wav')
                count = 0

    return frame


def getEyeCloseStandAlone():
    predictor_path = os.path.join("shape_predictor_68_face_landmarks.dat")
    predictor = dlib.shape_predictor(predictor_path)
    detector = dlib.get_frontal_face_detector()
    cap = cv2.VideoCapture(0)

    count = 0
    SleepAlertTime = 2  # After two seconds eye close: Warning drowsiness

    while True:
        suc, frame = cap.read()
        faces = detector(frame)

        if faces:
            landmarks = predictor(frame, faces[0])

            for i in range(0, 68):
                x = landmarks.part(i).x
                y = landmarks.part(i).y
                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

            EAR_avg = getEAR(landmarks)
            if EAR_avg > 0.4:
                cv2.putText(frame, "Eye's open", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                count = 0
            else:
                cv2.putText(frame, "Eye's closed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                count = count + 1

                if count >= SleepAlertTime * 30:  # Assumed almost 2 seconds
                    playsound('DrowsyWarning.wav')
                    count = 0

            print(EAR_avg)

        # frame = cv2.resize(frame, (round(frame.shape[1]/1.4), round(frame.shape[0]/1.4)))
        cv2.imshow("Live", frame)
        cv2.waitKey(1)

