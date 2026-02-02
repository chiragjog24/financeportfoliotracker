#!/bin/bash
# Database reset script for local development
# This script stops the database container, removes the volume, and restarts it

set -e

echo "Resetting local PostgreSQL database..."

# Stop and remove the database container
docker-compose stop db
docker-compose rm -f db

# Remove the database volume
docker volume rm financeportfoliotracker_postgres_data 2>/dev/null || echo "Volume already removed or doesn't exist"

# Start the database container
echo "Starting fresh database container..."
docker-compose up -d db

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 5

# Run migrations
echo "Running database migrations..."
alembic upgrade head

echo "Database reset complete!"
