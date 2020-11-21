# Use the Python3.7.2 image
#FROM python:3.7.2-stretch
FROM alpine:latest

RUN apk add --no-cache python3-dev && \
    pip3 install --upgrade pip

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
COPY . /app

# Install the dependencies
RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 8000

# run the command to start uWSGI
CMD ["gunicorn", "app_flask:app", "-c", "./gunicorn.conf.py"]
