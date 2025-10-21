#!/bin/sh
set -e

# Apply database migrations
python manage.py migrate

if [ "$DJANGO_PRODUCTION" = "1" ]; then
  # Start Gunicorn for production
  exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
else
  # Start Django development server
  exec python manage.py runserver 0.0.0.0:8000
fi
