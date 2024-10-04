# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
# COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip3 install pandas numpy pymysql plotly datetime statistics flask python-dotenv

# Copy the rest of the application code to the working directory
COPY . /app

# Expose the port that the application will run on
EXPOSE 5000

# Set environment variables