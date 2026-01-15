#!/bin/bash
set -e
exec > >(tee -a /var/log/myapp/start.log) 2>&1

echo "ApplicationStart: Starting application at $(date)"

# Change to app directory
cd /var/www/myapp

# Verify app.py exists
if [ ! -f app.py ]; then
    echo "ERROR: app.py not found in $(pwd)"
    ls -la
    exit 1
fi

# Start gunicorn
echo "Starting gunicorn..."
nohup gunicorn --bind 0.0.0.0:8000 --workers 3 --daemon app:app

# Wait for startup
sleep 5

# Verify process is running
if pgrep -f gunicorn > /dev/null; then
    echo "Application started successfully"
    ps aux | grep gunicorn
    exit 0
else
    echo "ERROR: Failed to start application"
    exit 1
fi
