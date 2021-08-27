# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# Updating apt to see and install Google Chrome
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE_92.0.4515`/chromedriver_linux64.zip  
RUN unzip /tmp/chromedriver.zip chromedriver -d ./

#Set up Environment variables
ENV DRIVER_PATH=/chromedriver

# copy the dependencies file to the working directory
COPY requirements.txt .
# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local directory to the working directory
COPY src/ .

# command to run on container start
CMD [ "python", "./main.py" ]