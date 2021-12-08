
# Base image
FROM python3

# Install python and pip
RUN apk add --upgrate py3-pip

#Upgrade pip
RUN pip install --upgrade pip

# Install python modules needed by the python add
COPY requirements.txt ./

# Copy files required for the app to run
COPY Fingers/. ./
COPY Functions/. ./
COPY Images/. ./
COPY HandTrackingModule.py ./
COPY trainMenu.py ./

# Tell the port number the container should run
EXPOSE 5000

# Run the application
CMD ["python", "Main_PersonalTrainer.py"]
