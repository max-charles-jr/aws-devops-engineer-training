#!/bin/bash
cd /var/www/myapp
export ENVIRONMENT=production
nohup python3 app.py > /var/log/myapp.log 2>&1 &
