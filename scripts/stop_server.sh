#!/bin/bash
exec > >(tee -a /var/log/myapp/stop.log) 2>&1

echo "ApplicationStop: Stopping application at $(date)"

# Stop any running gunicorn processes
pkill -f gunicorn || true
pkill -f "python.*app.py" || true

# Wait for processes to stop
sleep 2

echo "Application stopped"
exit 0
