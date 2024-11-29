# Use an official Python runtime as a parent image
#FROM --platform=arm64 python:3.10-slim
FROM python:3.11-slim

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]