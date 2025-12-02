#!/usr/bin/env bash

echo "🚀 Starting ChamaNexus Backend..."

# Wait a moment for database
sleep 2

# Run database migrations
echo "📦 Running database migrations..."
python manage.py migrate --noinput

# Create superuser if not exists (optional, remove in production)
echo "👤 Checking superuser..."
python manage.py shell << EOF
from accounts.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        email='admin@chamanexus.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print("✅ Superuser created: admin@chamanexus.com / admin123")
else:
    print("✅ Superuser already exists")
EOF

# Collect static files (if not done in build)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput || true

# Start Gunicorn with timeout settings
echo "🌐 Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:10000 \
    --workers 2 \
    --worker-class sync \
    --timeout 120 \
    --keep-alive 5 \
    --access-logfile - \
    --error-logfile -
