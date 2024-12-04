# Base image with Python 3.12
FROM python:3.12-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the application files
COPY ./app .

# Install Python dependencies globally
RUN pip install --no-cache-dir -r /app/requirements.txt


# Set the default command (overridden if necessary in docker-compose.yml)
CMD ["python", "producer.py"]
