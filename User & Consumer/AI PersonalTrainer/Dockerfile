# Base image
FROM python3

# Install python and pip
RUN apk add --upgrate py3-pip
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*


#Upgrade pip
RUN pip install --upgrade pip

# Install python modules needed by the python add
COPY requirements.txt ./

# Copy files required for the app to run
COPY Fingers/. ./
COPY Functions/. ./
COPY Images/. ./
COPY HandTrackingModule.py ./
COPY Functions/trainMenu.py ./

# Tell the port number the container should run
EXPOSE 5000

RUN pip3 install --no-cache-dir -r /requirements.txt

# Run the application
CMD ["python", "Main_PersonalTrainer.py"]
