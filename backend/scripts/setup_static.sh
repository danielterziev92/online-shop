#!/bin/sh
# Setup staticfiles directory with proper permissions

# Set -e to exit on error
set -e

# Define static files directory
STATIC_DIR=${1:-"${APP_HOME}/staticfiles"}

echo "Setting up static files directory: $STATIC_DIR"

# Create the directory if it doesn't exist
mkdir -p "$STATIC_DIR"

echo "Static files directory setup complete."