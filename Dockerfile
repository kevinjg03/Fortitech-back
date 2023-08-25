# Using lightweight alpine image
FROM python:3.11-alpine

# Installing packages
RUN apk update
RUN pip install twilio flask flask-restful Flask-Migrate psycopg2-binary numpy

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY app ./app

# Start app
EXPOSE 5001
ENTRYPOINT python ./app/index.py
