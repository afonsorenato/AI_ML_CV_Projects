# just some safeguard code for eye and face detection

import cv2
import numpy as np
import time
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from itertools import product, combinations

face_cascade = cv2.CascadeClassifier('haar\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haar\haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
a = 290
b = 250
c = 200
d = 105

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        #cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #cv2.putText(gray, 'Renato', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (100, 0, 255), 1)
        #cv2.rectangle(img, (a, b), (a + c, b + d), (255, 0, 0), 2) #eye box
        #cv2.putText(img, 'HUD Eye-box', (a, b - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            if ((a < (ex+x) and (x+ex+ew > a)) and (a+c > (ex+x) and (x+ex+ew < a+c))) and ((b < (ey+y) and (y+ey+eh > b)) and (b+d > (ey+y) and (y+ey+eh < b+d))):
                cv2.putText(img, 'Driver inside the Eye-box', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 20, 12), 1)
            else:
                cv2.putText(img, 'Driver outide the Eye-box', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 25, 12), 1)

    #cv2.imshow('img', img)
    #key = cv2.waitKey(200)

#-----------------Design cabin----------------------------------------------------------------------------
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # draw cabin
    rx = [-8, 0]
    ry = [-4, 4]
    rz = [0, 8]

    # center = 2 + (-2) / 2
    for s, e in combinations(np.array(list(product(rx, ry, rz))), 2):
        if np.sum(np.abs(s - e)) == rx[1] - rx[0]:
            ax.plot3D(*zip(s, e), color="b")

    # draw camera
    rrx = [-0.5, 0.5]  # centro em zero - origem referencial
    rry = [-0.5, 0.5]
    rrz = [-0.5, 0.5]
    # center = 2 + (-2) / 2
    for ss, ee in combinations(np.array(list(product(rrx, rry, rrz))), 2):
        if np.sum(np.abs(ss - ee)) == rrx[1] - rrx[0]:
            ax.plot3D(*zip(ss, ee), color="g")

    # draw a point
    ax.scatter([0], [0], [0], color="g", s=100)

    # draw windshield
    ii = [-6, -4, -2, 0, 2, 4, 6]
    for ii in ii:
        x = [5, -4]
        y = [ii, ii]
        z = [0, 5]
        figure = ax.plot(x, y, z, c='r')

    plt.show()
    time.sleep(1)
    plt.close('all')
    key = cv2.waitKey(20)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


