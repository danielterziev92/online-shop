#!/bin/sh
# Master initialization script that runs all setup scripts in sequence

# Set -e to exit on error
set -e

echo "🚀 Initializing application..."

# 1. Setup logs directory
echo "📋 Setting up logs directory..."
. "${SCRIPTS_PATH}/setup_logs.sh" "${LOGS_PATH:-"$APP_HOME/logs"}"

# 2. Setup static files directory
echo "📦 Setting up static files directory..."
. "${SCRIPTS_PATH}/setup_static.sh" "${STATIC_PATH:-"$APP_HOME/staticfiles"}"

# 3. Collect static files
echo "🔍 Collecting static files..."
. "${SCRIPTS_PATH}/collect_static.sh" "${STATIC_PATH:-"$APP_HOME/staticfiles"}"

# Run any additional initialization commands
echo "✅ Application initialization complete!"
exec "${SCRIPTS_PATH}/initialize.sh"