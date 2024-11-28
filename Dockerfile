# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory (default to /app in Docker, but Azure uses /home/site/wwwroot)
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container (except data-files)
COPY . .

# Copy the Excel file into the /home directory, used for persistent storage in Azure
COPY data-files/Bilabonnement_2024_Clean.xlsx /home/

# Set file permissions for the Excel file
RUN chmod 644 /home/Bilabonnement_2024_Clean.xlsx

# Run app.py when the container launches with gunicorn (HTTP server)
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]