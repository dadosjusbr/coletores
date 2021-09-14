FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local mpba directory to the working directory
COPY mpba/ .

# copy the content of the local roles.csv file to the working directory 
COPY roles.csv .

# command to run on container start
CMD ["python", "./main.py"]
