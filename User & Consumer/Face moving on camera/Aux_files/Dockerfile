
FROM python:3.6

ADD ../Main_faceInSystemDlib.py .
ADD methods.py .
ADD haarcascade_eye.xml .
ADD haarcascade_frontalface_default.xml .
ADD shape_predictor_68_face_landmarks.dat .
ADD Video1.mp4 .

# Execute the linux commands
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install -U pip wheel cmake
RUN pip install opencv-python
RUN pip install dlib
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y



# Start the app with node
CMD ["python", "./Main_faceInSystemDlib.py"]