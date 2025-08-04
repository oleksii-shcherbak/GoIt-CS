#!/bin/bash

echo "=== GoIT CS Homework 06 - Web Application ==="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Stop any existing containers
echo "Stopping existing containers..."
docker compose down 2>/dev/null || docker-compose down 2>/dev/null

# Build and run the application in background
echo "Building and starting the application..."
echo ""

# Run in detached mode
if command -v docker-compose &> /dev/null; then
    docker-compose up --build -d
else
    docker compose up --build -d
fi

# Wait for services to start
echo "Waiting for services to start..."
sleep 5

# Open browser
echo "Opening browser..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://localhost:3000
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open http://localhost:3000 2>/dev/null || echo "Please open http://localhost:3000 manually"
fi

echo ""
echo "Application is running at http://localhost:3000"
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
