#!/bin/bash
set -e
exec > >(tee -a /var/log/myapp/before_install.log) 2>&1

echo "BeforeInstall: Preparing environment at $(date)"

# Create application directory
mkdir -p /var/www/myapp
chown ec2-user:ec2-user /var/www/myapp
chmod 755 /var/www/myapp

# Create log directory
mkdir -p /var/log/myapp
chown ec2-user:ec2-user /var/log/myapp
chmod 755 /var/log/myapp

# Clean up old deployments (optional)
# rm -rf /var/www/myapp/*

echo "Environment prepared successfully"
