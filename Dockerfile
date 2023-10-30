# md-apisecurity/Dockerfile

FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /app

# Arguments
ARG FLASK_ENV
ARG TESTING
ARG FLASK_DEBUG

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the requirements file
COPY src/requirements.txt /app/src/requirements.txt
RUN apt-get -y update && apt-get install -y curl iputils-ping

# Install the dependencies
RUN pip3 install -r src/requirements.txt

# Copy the rest of the application files
COPY . /app/

# Labels
LABEL author="d.zunigab@uniandes.edu.co"
LABEL module="md-apisecurity"

# Flask environment variables
ENV FLASK_APP="src/app.py"
ENV FLASK_ENV=${FLASK_ENV}
ENV TESTING=${TESTING}
ENV FLASK_DEBUG=${FLASK_DEBUG}
ENV FLASK_APP_NAME="core-apiuser"
ENV PYTHONPATH="./"

# Expose the port the app will run on
EXPOSE 9003

# Run the command to start the app
CMD [ "gunicorn", "-w", "2", "manage:app", "-b", "0.0.0.0:9003", "--log-level", "debug" ]