#!/bin/sh

# Create the staticfiles directory if it doesn't exist
mkdir -p /code/staticfiles

# Make database migrations
python manage.py makemigrations

# Run database migrations
python manage.py migrate --noinput

# Create a superuser
python manage.py su

# Collect static files (if needed)
python manage.py collectstatic --noinput

# Start the Gunicorn server
gunicorn --bind 0.0.0.0:8000 dukeverse.wsgi:application