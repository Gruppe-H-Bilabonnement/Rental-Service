# Use an official Python runtime as a parent image
#FROM python:3.9-slim
FROM --platform=arm64 python:3.9-slim 

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Run app.py when the container launches with gunicorn (HTTP server)
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
