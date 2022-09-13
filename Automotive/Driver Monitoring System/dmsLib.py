import numpy as np
import cv2, pickle
import os, dlib, time

from playsound import playsound
from Aux_Files import *
from Aux_Files import DriverID

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
THICKNESS = 2


def getModelsParameters():
    predictor_path = os.path.join("Others/shape_predictor_68_face_landmarks.dat")
    predictor = dlib.shape_predictor(predictor_path)
    detector = dlib.get_frontal_face_detector()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("Others/trainner.yml")
    net = cv2.dnn.readNet("Others/yolov3-tiny.weights", "Others/yolov3-tiny.cfg")

    return net, predictor_path, predictor, detector


# Coeficient to assess the user's state of alert based on eyes
def getEAR(landmarks):
    # Get EAR - ||p2-p6|| + ||p3-p5||)/(2*||p1-p4||
    p1 = (landmarks.part(36).x, landmarks.part(36).y)
    p2 = (landmarks.part(37).x, landmarks.part(37).y)
    p3 = (landmarks.part(38).x, landmarks.part(38).y)
    p4 = (landmarks.part(39).x, landmarks.part(39).y)
    p5 = (landmarks.part(40).x, landmarks.part(40).y)
    p6 = (landmarks.part(41).x, landmarks.part(41).y)
    EAR_right = (norma(p2, p6) + norma(p3, p5)) / (2 * (norma(p1, p4)))

    p1 = (landmarks.part(42).x, landmarks.part(42).y)
    p2 = (landmarks.part(43).x, landmarks.part(43).y)
    p3 = (landmarks.part(44).x, landmarks.part(44).y)
    p4 = (landmarks.part(45).x, landmarks.part(45).y)
    p5 = (landmarks.part(46).x, landmarks.part(46).y)
    p6 = (landmarks.part(47).x, landmarks.part(47).y)
    EAR_left = (norma(p2, p6) + norma(p3, p5)) / (2 * (norma(p1, p4)))

    return (EAR_left + EAR_right) / 2


# If the user's eyes are closed, then outputs an audio warning
def getEyeClose(frame, predictor_path, predictor, detector, count):
    SleepAlertTime = 2  # After two seconds eye close: Warning drowsiness
    faces = detector(frame)

    if faces:
        landmarks = predictor(frame, faces[0])

        EAR_avg = getEAR(landmarks)
        if EAR_avg > 0.25:
            cv2.putText(frame, "Eye's open", (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, GREEN, THICKNESS, cv2.LINE_AA)
            count = 0
            frame = getOrientation(frame, detector, predictor)
        else:
            cv2.putText(frame, "Eye's closed", (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, RED, THICKNESS, cv2.LINE_AA)
            count = count + 1
            for i in range(0, 68):
                x = landmarks.part(i).x
                y = landmarks.part(i).y
                frame = cv2.circle(frame, (x, y), 2, RED, -1)

            if count >= SleepAlertTime * 30:  # Assumed almost 2 seconds
                # playsound('Others/DrowsyWarning.wav')
                cv2.putText(frame, "WARNING! SLEEPY!", (400, 400),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, THICKNESS, 10, cv2.LINE_AA)

                count = 0

    return frame, count


# Outputs user orientation: left, front and right
def getOrientation(image, detector, predictor):
    img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    faces = detector(img_gray)

    if faces:
        landmarks = predictor(image, faces[0])

        rat1 = abs(landmarks.part(39).x - landmarks.part(27).x)
        rat2 = abs(landmarks.part(42).x - landmarks.part(27).x) + 0.01
        rat = rat1 / rat2

        if (rat >= 2.5):
            str = "Looking to the left"
            color = RED
        elif (rat <= 0.4):
            str = "Looking to the right"
            color = RED
        else:
            str = "Looking forward"
            color = GREEN

        cv2.putText(image, str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, THICKNESS, cv2.LINE_AA)

        for i in range(1, 68):
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            cv2.circle(image, (x, y), 2, color, -1)

    return image


# Allows to detect a cellphone
def getCellPhone(img, net, classes, color):
    layer_names = net.getLayerNames()
    outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, chan = img.shape
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(outputlayers)
    boxes = []
    confidences = []
    class_ids = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            if class_ids[i] > 1:
                cv2.rectangle(img, (x, y), (x + w, y + h), RED, THICKNESS)
                cv2.putText(img, label, (x, y - 10), font, 1, RED, 1)
                color = RED

    return img, color


# Pose estimator
def getHeadPose(image, predictor, detector):
    height = image.shape[0]
    width = image.shape[1]
    size = image.shape

    img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    faces = detector(img_gray)

    if faces:
        landmarks = predictor(image, faces[0])

        for i in [8, 34, 41, 46, 60, 54]:
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            cv2.circle(image, (x, y), THICKNESS, RED, -1)

        # 3D model points of the face
        model_points = np.array([
            (0.0, 0.0, 0.0),  # Nose tip - 34
            (0.0, -330.0, -65.0),  # Chin - 9
            (-225.0, 170.0, -135.0),  # Left eye left corner - 46
            (225.0, 170.0, -135.0),  # Right eye right corne - 37
            (-150.0, -150.0, -125.0),  # Left Mouth corner - 55
            (150.0, -150.0, -125.0)  # Right mouth corner - 49
        ])

        # Same points on the frame: with landmarks
        image_points = np.array([
            (landmarks.part(33).x, landmarks.part(33).y),  # nose tip
            (landmarks.part(9).x, landmarks.part(9).y),  # chin
            (landmarks.part(46).x, landmarks.part(46).y),  # left eye left corner
            (landmarks.part(37).x, landmarks.part(37).y),  # right eye right corner
            (landmarks.part(55).x, landmarks.part(55).y),  # left mouth corner
            (landmarks.part(49).x, landmarks.part(49).y),  # right mouth corner
        ], dtype="double")

        # Camera internals
        focal_length = size[1]
        center = (size[1] / 2, size[0] / 2)
        camera_matrix = np.array([[focal_length, 0, center[0]], [0, focal_length, center[1]], [0, 0, 1]],
                                 dtype="double")

        dist_coeffs = np.zeros((4, 1))  # Assuming no lens dist
        (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                      dist_coeffs)
        print(rotation_vector[1])
        # rotation_vector[1] = rotation_vector[1]
        (nose_end_point2D, jacobian) = cv2.projectPoints(
            np.array([(0.0, 0.0, 500.0)]),
            rotation_vector, translation_vector,
            camera_matrix, dist_coeffs)

        p1 = (int(image_points[0][0]), int(image_points[0][1]))
        p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
        cv2.line(image, p1, p2, BLUE, THICKNESS)

    return image


# Welcome function
def welcomeFunction(cap):
    name = "Unknown"
    flag = False

    while flag is False:
        ret, frame = cap.read()
        cv2.imshow("Image", frame)
        cv2.waitKey(2000)

        if name == "Unknown":
            name = DriverID.getDriverID(frame, labels, recognizer)
        else:
            flag = True
            cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, RED, THICKNESS, cv2.LINE_AA)
            cv2.imshow("Image", frame)
            cv2.waitKey(2000)
            print(name)
            print("You can ignite the car\n")
            playsound('WelcomeToCar.wav')
            cv2.destroyAllWindows()

    return name


def norma(a, b):
    c = a[0] - b[0]
    d = a[1] - b[1]
    y = (c, d)
    return np.sqrt(y[0] * y[0] + y[1] * y[1])


def getLabels():
    labels = {}
    with open("Others/labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}

    return labels


def getClasses():
    with open("Others/coco.names.txt", 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    return classes
