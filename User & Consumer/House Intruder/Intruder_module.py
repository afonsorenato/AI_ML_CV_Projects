import sys, os, cv2
import numpy as np
import smtplib, ssl, email

from email import encoders
from getpass import getpass
from redmail import EmailSender
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# Paths
path_classes = '../House Intruder/Weights/coco.names'
path_weights = '../House Intruder/Weights/yolov3-tiny.weights'
path_config = '../House Intruder/Weights/yolov3-tiny.cfg'


# read class names from text file
def getClasses(path):
    classes = None
    path = '../House Intruder/Weights/coco.names'
    with open(path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    return classes


def get_output_layers(net):
    layer_names = net.getLayerNames()

    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


@getClasses
def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), (0,0,255), 2)
    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
    return img



def getPrediction(image):

    human_detected = False

    # initialization
    out_image = image
    class_ids, confidences,boxes = [], [], []
    conf_threshold, nms_threshold = 0.5, 0.4
    Width, Height = image.shape[1], image.shape[0]

    net = cv2.dnn.readNet(path_weights, path_config)
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416,416), (0,0,0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                human_detected = True
                print("Human detected")

    return out_image, human_detected



def enterPassword():
    password = "test_python"
    return password



def sendEmail(password):

    sender_email = "python.cv.experiments@gmail.com"
    receiver_email = "afonsorenato96@gmail.com"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, "Intruder detected")

    print("Email sent...")



def sendImageEmail():
    email = EmailSender(host="smtp.myhost.com", port=1)

    email.send(
        sender="python.cv.experiments@gmail.com",
        subject="Intruder warning",
        receivers=["afonsorenato96@gmail.com"],
        html="""
            <h1>Hi, take a look at this image:</h1>
            {{ my_image }}
        """,
        body_images={"my_image": "IntruderSnapShot.jpg"}
    )







