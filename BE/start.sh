#!/usr/bin/env bash
# Start Gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3
