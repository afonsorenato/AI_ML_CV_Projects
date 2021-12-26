# Identifies a face and the eyes
# Tells if user is inside or outside the eye-box
# Indicates which area of the eye-box is in: 1, 2 or 3

"""
#Open Points
-> calibrate the variation of eye-box size vs user distance: variation factor
-> camera calibration to get focal distance: use real chessboards and verify square's size
-> Verify distance face estimation (compare / measure it in bench)
"""
import cv2
from Aux_files import methods
import dlib

face_ref = 12

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("Aux_files/shape_predictor_68_face_landmarks.dat")

face_cascade = cv2.CascadeClassifier('Aux_files/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('Aux_files/haarcascade_eye.xml')

#video = cv2.VideoCapture(0)
video = cv2.VideoCapture("Aux_files/Video1.mp4")
check, img = video.read()

while True:

    check, img = video.read()

    if check is False:
        break

    img = cv2.resize(img, (800, 450))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(img, (x, y), 2, (255, 0, 0), -1)

        w = landmarks.part(16).x - landmarks.part(0).x
        faceDist = methods.getFaceDist(w, face_ref)
        xx, yy, ww, hh = methods.drawEyeBoxSize(faceDist, img)
        methods.printCalibPositionDlib(img, landmarks.part(27).x, landmarks.part(36).x,
                                       landmarks.part(45).x, xx, yy, ww)

    cv2.imshow("Capturing", img)
    key = cv2.waitKey(10)

    if key == ord('q'):
        break

video.release()
