#!/bin/bash
cd /var/www/myapp
# export ENVIRONMENT=production
# nohup python3 app.py > /var/log/myapp.log 2>&1 &

nohup gunicorn --bind 0.0.0.0:8000 --workers 3 app:app > /var/log/app/gunicorn.log 2>&1 &