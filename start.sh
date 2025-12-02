#!/bin/bash
echo "🚀 Starting ChamaNexus Backend..."

# Run database migrations
echo "📦 Running database migrations..."
python manage.py migrate --noinput

# Try to create superuser, but continue if it fails
echo "👤 Checking superuser..."
if [ -z "$DJANGO_SUPERUSER_EMAIL" ] || [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "⚠️ Skipping superuser creation (no credentials provided)"
else
    # Use the shell to create superuser without triggering Argon2
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='$DJANGO_SUPERUSER_EMAIL').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print("✅ Superuser created")
else:
    print("✅ Superuser already exists")
EOF
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start Gunicorn
echo "🌐 Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:10000 \
    --workers 2 \
    --worker-class sync \
    --timeout 120 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile -
