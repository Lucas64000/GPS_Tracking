#!/bin/bash

# Function to display messages with a consistent format
log() {
    echo -e "\n\033[1;32m[INFO]\033[0m $1\n"
}

# Step 1: Stop and remove any running containers
log "Stopping and removing existing containers..."
docker-compose down

# Step 2: Build the services
log "Building Docker services..."
docker-compose build

# Step 3: Start the services
log "Starting Docker services..."
docker-compose up -d

# Step 4: Display logs for producer1, producer2, and consumer
log "Displaying logs for producer1, producer2, and consumer..."
docker logs -f whereismydad-producer1  &
docker logs -f whereismydad-producer2  &
docker logs -f whereismydad-consumer 

# Step 5: Open Kafka UI in the browser
log "Kafka UI available at http://localhost:7777"
