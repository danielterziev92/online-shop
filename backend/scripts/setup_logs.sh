#!/bin/sh
# Setup logs directory with proper permissions

# Set -e to exit on error
set -e

# Define logs directory
LOGS_DIR=${1:-"$APP_HOME/logs"}

echo "Setting up logs directory: $LOGS_DIR"

# Create logs directory if it doesn't exist
mkdir -p "$LOGS_DIR"

# Skip chown operations if running as non-root
if [ "$(id -u)" = "0" ]; then
    # Set ownership to appuser (as defined in Dockerfile)
    chown -R appuser:appuser "$LOGS_DIR" || echo "Warning: Could not change ownership of $LOGS_DIR"
else
    echo "Running as non-root user, skipping ownership changes"
fi

# Set full permissions for the logs directory and all files inside (read/write/execute for all)
# 777 = rwxrwxrwx (read, write, execute for owner, group, and others)
chmod -R 777 "$LOGS_DIR" 2>/dev/null || echo "Warning: Could not change permissions of $LOGS_DIR"

echo "Logs directory setup complete."