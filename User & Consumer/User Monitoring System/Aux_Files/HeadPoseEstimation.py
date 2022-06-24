import os
import dlib
import numpy as np
import math
import cv2
import time

predictor_path = os.path.join("shape_predictor_68_face_landmarks.dat")
predictor = dlib.shape_predictor(predictor_path)
detector = dlib.get_frontal_face_detector()

def getHeadPose(image):
    predictor_path = os.path.join("shape_predictor_68_face_landmarks.dat")
    predictor = dlib.shape_predictor(predictor_path)
    detector = dlib.get_frontal_face_detector()

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
            cv2.circle(image, (x, y), 2, (0, 0, 255), -1)

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
        camera_matrix = np.array([[focal_length, 0, center[0]],
                                  [0, focal_length, center[1]],
                                  [0, 0, 1]], dtype="double")

        dist_coeffs = np.zeros((4, 1))  # Assuming no lens dist
        (success, rotation_vector, translation_vector) = cv2.solvePnP(
            model_points, image_points, camera_matrix,
            dist_coeffs)

        # rotation_vector[1] = rotation_vector[1]
        (nose_end_point2D, jacobian) = cv2.projectPoints(
            np.array([(0.0, 0.0, 500.0)]),
            rotation_vector, translation_vector,
            camera_matrix, dist_coeffs)

        #print(rotation_vector)

        p1 = (int(image_points[0][0]), int(image_points[0][1]))
        p2 = (int(nose_end_point2D[0][0][0]),
              int(nose_end_point2D[0][0][1]))
        cv2.line(image, p1, p2, (255, 0, 0), 2)

    return image

def getHeadPoseStandalone():
    predictor_path = os.path.join("shape_predictor_68_face_landmarks.dat")
    predictor = dlib.shape_predictor(predictor_path)
    detector = dlib.get_frontal_face_detector()

    cap = cv2.VideoCapture(0)

    while True:
        suc, image = cap.read()
        height = image.shape[0]
        width = image.shape[1]
        size = image.shape
        start = time.time()
        img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        faces = detector(img_gray)

        if faces:
            landmarks = predictor(image, faces[0])

            for i in [8, 34, 41, 46, 60, 54]:
                x=landmarks.part(i).x
                y=landmarks.part(i).y
                cv2.circle(image, (x, y), 2, (0, 0, 255), -1)

            #Head pose estimation-----------------------------------

            #3D model points of the face
            model_points = np.array([
                (0.0, 0.0, 0.0),  # Nose tip - 34
                (0.0, -330.0, -65.0),  # Chin - 9
                (-225.0, 170.0, -135.0),  # Left eye left corner - 46
                (225.0, 170.0, -135.0),  # Right eye right corne - 37
                (-150.0, -150.0, -125.0),  # Left Mouth corner - 55
                (150.0, -150.0, -125.0)  # Right mouth corner - 49
             ])

            #Same points on the frame: with landmarks
            image_points = np.array([
                (landmarks.part(33).x, landmarks.part(33).y), #nose tip
                (landmarks.part(9).x, landmarks.part(9).y), #chin
                (landmarks.part(46).x, landmarks.part(46).y), #left eye left corner
                (landmarks.part(37).x, landmarks.part(37).y), #right eye right corner
                (landmarks.part(55).x, landmarks.part(55).y), #left mouth corner
                (landmarks.part(49).x, landmarks.part(49).y), #right mouth corner
            ], dtype="double")

            #Camera internals
            focal_length = size[1]
            center = (size[1]/2, size[0]/2)
            camera_matrix = np.array([[focal_length, 0, center[0]],
                                    [0, focal_length, center[1]],
                                    [0, 0, 1]], dtype = "double")


            dist_coeffs = np.zeros((4,1)) # Assuming no lens dist
            (success, rotation_vector, translation_vector) = cv2.solvePnP(
                model_points, image_points, camera_matrix,
                dist_coeffs)

            #rotation_vector[1] = rotation_vector[1]
            (nose_end_point2D, jacobian) = cv2.projectPoints(
                np.array([(0.0, 0.0, 500.0)]),
                rotation_vector, translation_vector,
                camera_matrix, dist_coeffs)

            #print(rotation_vector)

            p1 = (int(image_points[0][0]), int(image_points[0][1]))
            p2 = (int(nose_end_point2D[0][0][0]),
                  int(nose_end_point2D[0][0][1]))
            cv2.line(image, p1, p2, (255, 0, 0), 2)

        #Final print
        end = time.time()
        print("Total time:", end-start)
        image = cv2.resize(image, (round(width/1.4), round(height/1.4)))
        cv2.imshow('Renato', image)
        cv2.waitKey(1)

def getOrientation(image, detector, predictor):
    img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    faces = detector(img_gray)

    if faces:
        landmarks = predictor(image, faces[0])

        rat1 = abs(landmarks.part(39).x - landmarks.part(27).x)
        rat2 = abs(landmarks.part(42).x - landmarks.part(27).x) + 0.01
        rat = rat1 / rat2

        if(rat >= 2.5):
            str = "Looking to the left"
            color = (0, 0, 255)
        elif(rat<= 0.4):
            str = "Looking to the right"
            color = (0, 0, 255)
        else:
            str = "Looking forward"
            color = (0,255,0)

        cv2.putText(image, str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

        for i in range(1, 68):
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            cv2.circle(image, (x, y), 2, color, -1)

    return image





