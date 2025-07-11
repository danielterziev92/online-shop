#!/bin/sh
# Collect Django static files

# Set -e to exit on error
set -e

# Define static files directory
STATIC_DIR=${1:-"$APP_HOME/staticfiles"}

echo "Collecting static files..."

# Collect static files
python manage.py collectstatic --noinput

echo "✅ Static files collected successfully!"
TOTAL_FILES=$(find "$STATIC_DIR" -type f | wc -l)
echo "Total files collected: $TOTAL_FILES"

echo "Static files collection complete."