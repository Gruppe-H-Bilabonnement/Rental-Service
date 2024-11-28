FROM python:3.9-slim

# Set working directory
WORKDIR /home/site/wwwroot

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Copy the Excel file into the /home directory
COPY data-files/Bilabonnement_2024_Clean.xlsx /home/Bilabonnement_2024_Clean.xlsx

# Set file permissions (optional, to ensure accessibility)
RUN chmod 644 /home/Bilabonnement_2024_Clean.xlsx

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]