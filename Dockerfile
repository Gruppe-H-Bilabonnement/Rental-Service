# Use an official Python runtime as a parent image
#FROM --platform=arm64 python:3.10-slim
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt into the container
COPY requirements.txt .

# Upgrade pip and install requirements
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

#COPY Bilabonnement_2024_Clean.xlsx /home/Bilabonnement_2024_Clean.xlsx

# Expose the port the app runs on
EXPOSE 80

# Run app.py when the container launches with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]