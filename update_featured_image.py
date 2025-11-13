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

# Image URL for Fender Precision Bass
image_url = "https://eddiesguitars.com/wp-content/uploads/2022/11/Fender-5-006.jpg"

# Get the Fender Precision Bass
featured_instrument = Instrument.objects.filter(name__icontains="Bass", brand__icontains="Fender", featured=True).first()

if featured_instrument:
    print(f"Updating image for: {featured_instrument.brand} {featured_instrument.name}")

    # Download the image
    response = requests.get(image_url)
    if response.status_code == 200:
        # Save the image to the instrument
        image_name = "fender-precision-bass-new.jpg"
        featured_instrument.image.save(image_name, File(BytesIO(response.content)), save=True)
        print(f"✓ Image updated successfully!")
        print(f"  Image saved as: {featured_instrument.image.url}")
    else:
        print(f"✗ Failed to download image. Status code: {response.status_code}")
else:
    print("✗ Fender Precision Bass not found in featured instruments")
