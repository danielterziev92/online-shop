#!/bin/sh
#Starts the Django application with necessary setup

# Exit on error
set -e

# Apply database migrations
echo "⚙️ Applying migrations..."
python manage.py migrate

# Create superuser if enabled
if [ "${CREATE_SUPERUSER:-true}" = "true" ]; then
    SUPERUSER_EMAIL=${SUPERUSER_EMAIL:-admin@example.com}
    SUPERUSER_PASSWORD=${SUPERUSER_PASSWORD:-admin123}
    
    echo "👤 Creating superuser..."
    python manage.py createsuperaccount --email $SUPERUSER_EMAIL --password $SUPERUSER_PASSWORD --noinput || echo "Superuser creation failed or already exists."
fi

# Generate sample data (optional)
if [ "${GENERATE_SAMPLE_DATA:-false}" = "true" ]; then
    echo "📊 Generating sample data..."
    python generate_sample_data.py
fi

# Start the server
echo "🚀 Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000