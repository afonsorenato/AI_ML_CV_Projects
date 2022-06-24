import cv2
import numpy as np
import face_recognition
import dlib
import pickle
import time
import os

# Used function on the Main file
def getDriverID(frame, labels, recognizer):
    #print("Entered driver ID function \n")
    name = ""
    face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')
    #recognizer = cv2.face.LBPHFaceRecognizer_create()
    #recognizer.read("trainner.yml")

    #labels = {}
    #with open("labels.pickle", 'rb') as f:
    #    og_labels = pickle.load(f)
    #    labels = {v:k for k,v in og_labels.items()}

    #cap = cv2.VideoCapture(0)
    #while True:
        #status, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5,minNeighbors=5)

    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y + h, x:x + w]

        #Recognize
        id_, conf = recognizer.predict(roi_gray)
        if conf >= 45:
            name = labels[id_]
            print(name)
            cv2.putText(frame, name, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
        else:
            name = "Unknown"
            print(name)
            cv2.putText(frame, name, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

        color = (255,0,0) #BGR
        stroke = 2
        end_cord_x = x+w
        end_cord_y = y+h
        cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)

    return name

        #cv2.imshow('frame', frame)
        #if cv2.waitKey(20) & 0xFF == ord('q'):
         #   break

    #Release everything done
    #cap.release()
    #cv2.destroyAllWindows()

# Untouched functions
def getDriverID_Standalone():
    face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainner.yml")

    labels = {}
    with open("labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        start = time.time()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5,minNeighbors=5)

        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y + h, x:x + w]

            #Recognize
            id_, conf = recognizer.predict(roi_gray)
            if conf >= 45:
                name = labels[id_]
                cv2.putText(frame, name, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, "Unknown", (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

            color = (255,0,0) #BGR
            stroke = 2
            end_cord_x = x+w
            end_cord_y = y+h
            cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)

        end = time.time()
        print("time to ID:", end-start)
        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
