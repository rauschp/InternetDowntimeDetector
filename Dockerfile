# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /

# copy the dependencies file to the working directory
COPY requirements.txt /requirements.txt

# install dependencies
RUN pip install -r requirements.txt

COPY . /

# command to run on container start
CMD [ "python", "src/main.py" ]