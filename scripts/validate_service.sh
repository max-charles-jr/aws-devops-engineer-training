#!/bin/bash
set -e
exec > >(tee -a /var/log/myapp/validate.log) 2>&1

echo "ValidateService: Validating service at $(date)"

# Wait for application to be ready
sleep 3

# Check if process is running
if ! pgrep -f gunicorn > /dev/null; then
    echo "ERROR: Gunicorn process not running"
    exit 1
fi

# Test HTTP endpoint
echo "Testing HTTP endpoint..."
if curl -f -s http://localhost:8000/ > /dev/null || curl -f -s http://localhost:8000/health > /dev/null; then
    echo "Service validation successful"
    curl -s http://localhost:8000/ || curl -s http://localhost:8000/health
    exit 0
else
    echo "ERROR: Service validation failed"
    echo "Checking logs..."
    tail -20 /var/log/myapp/start.log
    exit 1
fi
