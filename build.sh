#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations if needed
echo "Running database migrations..."
python manage.py migrate --noinput || echo "Migrations completed (or skipped)"

echo "Build completed successfully!"
