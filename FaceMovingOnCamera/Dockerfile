
FROM python:3

ADD Main_faceInSystemDlib.py .
ADD methods.py .

# Execute the linux commands
RUN pip install -U pip wheel cmake
RUN pip install opencv-python
RUN pip install dlib
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install me

# Start the app with node
CMD ["python", "./Main_faceInSystemDlib.py"]