"""
Management command to load initial data fixtures for deployment.
Usage: python manage.py load_initial_data
"""

import io
import os
import random
import textwrap

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management import call_command
from django.core.management.base import BaseCommand

from PIL import Image, ImageDraw, ImageFont


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
            ensure_instrument_images(self.stdout)
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

        ensure_instrument_images(self.stdout)


def ensure_instrument_images(stdout):
    """Generate placeholder images for instruments missing media files."""
    from store.models import Instrument

    media_path = os.path.join(settings.MEDIA_ROOT, "instruments")
    static_path = os.path.join(settings.BASE_DIR, "static", "instruments")
    os.makedirs(media_path, exist_ok=True)

    palette = [
        "#1f2937",
        "#374151",
        "#4338ca",
        "#7c3aed",
        "#0f766e",
        "#0369a1",
    ]

    font = ImageFont.load_default()

    def write_success(message: str) -> None:
        if hasattr(stdout, "style"):
            stdout.write(stdout.style.SUCCESS(message))
        else:
            stdout.write(f"{message}\n")

    for instrument in Instrument.objects.all():
        file_exists = False
        image_name = instrument.image.name if instrument.image and instrument.image.name else ""

        if image_name:
            try:
                file_exists = instrument.image.storage.exists(image_name)
            except Exception:
                file_exists = False

        if not file_exists and image_name:
            static_candidate = os.path.join(static_path, os.path.basename(image_name))
            if os.path.exists(static_candidate):
                with open(static_candidate, "rb") as f:
                    instrument.image.save(os.path.basename(image_name), ContentFile(f.read()), save=True)
                write_success(f"✓ Copied static image for {instrument.name}")
                continue

        if file_exists:
            continue

        title = instrument.name or "Instrument"
        subtitle = instrument.brand or "Dave's Music"
        slug = instrument.slug or f"instrument-{instrument.pk}"
        filename = f"{slug}.jpg"

        image = Image.new("RGB", (800, 800), random.choice(palette))
        draw = ImageDraw.Draw(image)

        text_lines = textwrap.wrap(title, width=20)
        y = 320
        for line in text_lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            draw.text(((800 - width) / 2, y), line, fill="white", font=font)
            y += height + 6

        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        draw.text(((800 - subtitle_width) / 2, 520), subtitle, fill="#cbd5f5", font=font)

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)

        instrument.image.save(filename, ContentFile(buffer.getvalue()), save=True)
        write_success(f"✓ Created placeholder image for {instrument.name}")
