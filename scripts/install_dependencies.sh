#!/bin/bash
set -e
exec > >(tee -a /var/log/myapp/install.log) 2>&1

echo "AfterInstall: Installing dependencies at $(date)"

# NOW we can cd to the app directory - files are there!
cd /var/www/myapp

# Verify requirements.txt exists
if [ ! -f requirements.txt ]; then
    echo "ERROR: requirements.txt not found in $(pwd)"
    ls -la
    exit 1
fi

# Install Python dependencies
echo "Installing Python packages..."
pip3 install -r requirements.txt

echo "Dependencies installed successfully"
