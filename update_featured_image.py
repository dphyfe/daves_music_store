"""
Script to update featured instrument with an image URL
"""

import os
import django
import requests
from io import BytesIO
from django.core.files import File

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daves_music_store.settings")
django.setup()

from store.models import Instrument

# Image URL for Korg Synthesizer
image_url = "https://cdn11.bigcommerce.com/s-py7p1m9g1d/images/stencil/1600x1600/products/13646/42890/main__08747.1636398212.png?c=2"

# Get the Korg Synthesizer
featured_instrument = Instrument.objects.filter(brand__icontains="Korg", name__icontains="Synthesizer").first()

if featured_instrument:
    print(f"Updating image for: {featured_instrument.brand} {featured_instrument.name}")

    # Download the image with browser headers
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(image_url, headers=headers)
    if response.status_code == 200:
        # Save the image to the instrument
        image_name = "korg-synthesizer.jpg"
        featured_instrument.image.save(image_name, File(BytesIO(response.content)), save=True)
        print(f"✓ Image updated successfully!")
        print(f"  Image served from: {featured_instrument.image_display_url}")
    else:
        print(f"✗ Failed to download image. Status code: {response.status_code}")
else:
    print("✗ Korg Synthesizer not found")
