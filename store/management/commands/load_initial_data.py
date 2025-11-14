"""
Management command to load initial data fixtures for deployment.
Usage: python manage.py load_initial_data
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = "Load initial data fixtures for Dave's World of Music"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force reload even if data already exists",
        )

    def handle(self, *args, **options):
        force = options.get("force", False)

        # Check if data already exists
        from store.models import Category, Instrument

        if not force and (Category.objects.exists() or Instrument.objects.exists()):
            self.stdout.write(self.style.WARNING("Data already exists in database. Use --force to reload fixtures."))
            return

        self.stdout.write(self.style.SUCCESS("Loading initial data fixtures..."))

        # Define fixtures to load in order
        fixtures = [
            "fixtures/categories.json",
            "fixtures/instruments.json",
        ]

        # Load each fixture
        for fixture in fixtures:
            if os.path.exists(fixture):
                self.stdout.write(f"Loading {fixture}...")
                try:
                    call_command("loaddata", fixture, verbosity=0)
                    self.stdout.write(self.style.SUCCESS(f"✓ {fixture} loaded successfully"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"✗ Error loading {fixture}: {str(e)}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠ Fixture not found: {fixture}"))

        self.stdout.write(self.style.SUCCESS("\n✓ Initial data loaded successfully!"))
