#!/bin/bash
# Download python
sudo apt-get install python3
# Download pip
sudo apt-get install python3-pip
# install chromedriver
# Download the Chrome Driver
wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE_92.0.4515`/chromedriver_linux64.zip
unzip /tmp/chromedriver.zip chromedriver -d ./
# install dependencies
pip install -r requirements.txt
