import sys, os, cv2
import numpy as np
import smtplib, ssl, email, imghdr

from email import encoders
from getpass import getpass
from redmail import EmailSender
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.message import EmailMessage
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
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), (0, 0, 255), 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return img


def getPrediction(image):
    human_detected = False

    # initialization
    out_image = image
    class_ids, confidences, boxes = [], [], []
    conf_threshold, nms_threshold = 0.5, 0.4
    Width, Height = image.shape[1], image.shape[0]

    net = cv2.dnn.readNet(path_weights, path_config)
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                human_detected = True

    return out_image, human_detected


def enterPassword():
    password = "test_python"
    return password


def sendEmail(password, frame):
    # Saves image of intruder to be sent
    saved_image = cv2.imwrite("IntruderSnapShot.jpg", frame)

    Sender_Email = "python.cv.experiments@gmail.com"
    Receiver_Email = "afonsorenato96@gmail.com"
    Password = password

    newMessage = EmailMessage()
    newMessage['Subject'] = "Intruder detection warning"
    newMessage['From'] = Sender_Email
    newMessage['To'] = Receiver_Email
    newMessage.set_content('An intruder was detected on your room!')

    with open('IntruderSnapShot.jpg', 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name

    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email, Password)
        smtp.send_message(newMessage)

    print("Warning email sent...")


def cleanImages(path):
    files_in_directory = os.listdir(path)
    print(files_in_directory)
    filtered_files = [file for file in files_in_directory if file.endswith(".jpg")]

    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

    print("All images cleaned: GDPR guaranteed. \n Goodbye!\n")
