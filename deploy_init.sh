#!/bin/bash
# Deployment initialization script for Dave's World of Music
# This script should be run after migrations during deployment

set -e  # Exit on error

echo "🎸 Dave's World of Music - Deployment Initialization"
echo "=================================================="

# Run migrations
echo "📦 Running database migrations..."
python manage.py migrate --noinput

# Load initial data
echo "📊 Loading initial data fixtures..."
python manage.py load_initial_data

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Create cache table (if needed)
# python manage.py createcachetable

echo "=================================================="
echo "✅ Deployment initialization complete!"
echo "🚀 Your store is ready to launch!"
