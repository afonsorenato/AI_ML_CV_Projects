#3d representation of a cabin, driver as blue sphere, the eye-box piramid and the windshield in red stripes

import cv2
import numpy as np
import time
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

import matplotlib.pyplot as plt
from itertools import product, combinations
import methods

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

while 1:
    #plt.ion()
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)


    #Draw things
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    rx = [-8, 0]
    ry = [-6, 2]
    rz = [0, 8]

    # center = 2 + (-2) / 2
    for s, e in combinations(np.array(list(product(rx, ry, rz))), 2):
        if np.sum(np.abs(s - e)) == rx[1] - rx[0]:
            ax.plot3D(*zip(s, e), color="b")

        # draw camera
        rrx = [-0.5, 0.5]  # centro em zero - origem referencial
        rry = [-0.5, 0.5]
        rrz = [-0.5, 0.5]

    for ss, ee in combinations(np.array(list(product(rrx, rry, rrz))), 2):
        if np.sum(np.abs(ss - ee)) == rrx[1] - rrx[0]:
            ax.plot3D(*zip(ss, ee), color="g")

    # draw a point
    ax.scatter([0], [0], [0], color="g", s=10)

    #draw eye-box piramid
    xp = 18
    v = np.array([[xp, -2, 0], [xp, -2, 2], [xp, 2, 2],  [xp, 2, 0], [-10, 0, 1]])
    ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])

    # generate list of sides' polygons of our pyramid
    verts = [ [v[0],v[1],v[4]], [v[0],v[3],v[4]], [v[2],v[1],v[4]], [v[2],v[3],v[4]], [v[0],v[1],v[2],v[3]]]
    ax.add_collection3d(Poly3DCollection(verts,facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))


    # draw windshield
    ii = [-6, -4, -2, 0, 2, 4]
    for ii in ii:
        x = [5, -4]
        y = [ii, ii]
        z = [0, 5]
        figure = ax.plot(x, y, z, c='r')

    #get eyes potential position-----------------------------------------
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # eye box

        x_aux = -2
        y_aux = round((((x + x + w) / 2) / 50 - 7), 2)
        z_aux = -round((((2*y+h)/2)/50-5), 2)
        point = [x_aux, y_aux, z_aux]
        print("Point: " + str(point))
        ax.scatter([x_aux], [y_aux], [z_aux], color="b", s=50)
        break

    plt.show(block=False)
    plt.pause(1)
    plt.close('all')

    key = cv2.waitKey(1)

    if key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

