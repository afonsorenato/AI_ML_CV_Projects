import cv2
import numpy as np

def WelcomeMenu(img):

    inv = 640
    img_w = 140
    img_h = 140
    size = (img_w, img_h)
    squat = cv2.resize(cv2.imread("Images/menu_squat.PNG"), size)
    leg = cv2.resize(cv2.imread("Images/menu_leg_raises.PNG"), size)
    push = cv2.resize(cv2.imread("Images/menu_push_up.PNG"), size)

    out = img
    out[0:img_h, 20:160] = squat
    cv2.putText(img, "1",(img_h, 25), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

    out[img_h+20:2*img_h+20, 20:160] = leg
    cv2.putText(img, "2",(img_h, 185), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

    out[2*img_h+40:3*img_h+40, 20:160] = push
    cv2.putText(img, "3",(img_h, 345), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)


    cv2.putText(img, "Choose your workout",(230, 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

    return out



