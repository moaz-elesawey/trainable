#!/usr/bin/sh
set -e

echo "Trainable Prestart..."

# Upgrading the database
flask db upgrade

echo "Database Migrate..."
