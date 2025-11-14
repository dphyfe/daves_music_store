"""
Deployment initialization script for Docker containers.
Run this after the container starts to set up the database.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daves_music_store.settings")
django.setup()

from django.core.management import call_command
from django.db import connection


def run_migrations():
    """Run database migrations."""
    print("📦 Running database migrations...")
    call_command("migrate", "--noinput")
    print("✓ Migrations complete")


def load_fixtures():
    """Load initial data fixtures."""
    print("📊 Loading initial data fixtures...")
    try:
        call_command("load_initial_data")
        print("✓ Fixtures loaded")
    except Exception as e:
        print(f"⚠ Warning: Could not load fixtures: {e}")
        print("  This is normal if data already exists.")


def collect_static():
    """Collect static files."""
    print("🎨 Collecting static files...")
    call_command("collectstatic", "--noinput", "--clear")
    print("✓ Static files collected")


def check_database():
    """Check if database connection is working."""
    print("🔌 Checking database connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


def main():
    """Main deployment initialization function."""
    print("=" * 60)
    print("🎸 Dave's World of Music - Deployment Initialization")
    print("=" * 60)

    # Check database connection
    if not check_database():
        sys.exit(1)

    # Run initialization steps
    try:
        run_migrations()
        load_fixtures()
        collect_static()

        print("=" * 60)
        print("✅ Deployment initialization complete!")
        print("🚀 Your store is ready to launch!")
        print("=" * 60)

    except Exception as e:
        print(f"✗ Deployment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
