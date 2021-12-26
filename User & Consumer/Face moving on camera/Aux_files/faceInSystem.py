#identifies a face and the eyes
#tells if user is inside or outside the eye-box
#indicates which area of the eye-box is in: 1, 2 or 3

"""
#Open Points
-> calibrate the variation of eye-box size vs user distance: variation factor
-> camera calibration to get focal distance: use real chessboards and verify square's size
-> Verify distance face estimation (compare / measure it in bench)
"""
import cv2
import methods

face_cascade = cv2.CascadeClassifier('haar\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haar\haarcascade_eye.xml')
video = cv2.VideoCapture(0)

while True:
    check, img = video.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        #cv2.rectangle(img, (a, b), (a + c, b + d), (255, 0, 0), 2) #eye box

        faceDist = methods.getFaceDist(w)
        xx, yy, ww, hh = methods.drawEyeBoxSize(faceDist, img)

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        centroid_eye_left = []

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            centroid_eye_left = (round(x + (ex+ew)/2), round(y + (ey+eh)/2))

            #Define Area of calibration
            methods.printCalibPosition(centroid_eye_left, img, xx, yy, ww, hh, x, y, ex, ey, ew, eh)

    cv2.imshow("Capturing", img)
    key = cv2.waitKey(20)

    if key == ord('q'):
        break

video.release()
cv2.destroyWindow()
