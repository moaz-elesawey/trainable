#!/usr/bin/sh
set -e

echo "Upgrading Database..."
flask db upgrade
echo "Database Upgraded Successfully."

python /app/initialize_data.py