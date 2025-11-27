#!/usr/bin/env bash
# build.sh - Render build script

set -o errexit  # Exit on error

echo "🔨 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📦 Collecting static files..."
python manage.py collectstatic --no-input --settings=config.settings

echo "🗄️ Running database migrations..."
python manage.py migrate --no-input --settings=config.settings

echo "✅ Build completed successfully!"
