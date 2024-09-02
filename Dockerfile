# Use an official Python runtime as a parent image
FROM python:3.12.4-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN apk add --no-cache \
    build-base \
    tesseract-ocr \
    tesseract-ocr-data \
    && python3 -m ensurepip \
    && pip3 install --no-cache --upgrade pip setuptools \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apk del build-base

# Set environment variable for Tesseract executable path
ENV TESSERACT_CMD=/usr/bin/tesseract

# Download the NLI model
RUN python download_nli.py

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]