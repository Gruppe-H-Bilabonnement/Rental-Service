# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory (default to /app in Docker, but Azure uses /home/site/wwwroot)
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents (including 'data-files' folder) into the container
COPY . .

# Ensure the 'data-files' directory is copied to the right location for Azure (this is key)
COPY data-files /home/site/wwwroot/data-files

# Run app.py when the container launches with gunicorn (HTTP server)
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]