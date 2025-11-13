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

# Image URL for Martin D-28 Dreadnought
image_url = "https://images.squarespace-cdn.com/content/v1/5f319a2ae54daa1e5f6b9fcb/1711215959092-E2RANDNGRK8T3CN3YY6H/Martin_Standard_Series_D28_Acoustic+Guitar_D_28_NEW_2024_Serial_Number_2829496_8925.jpg?format=2500w"

# Get the Martin Dreadnought
featured_instrument = Instrument.objects.filter(name__icontains="Dreadnought", brand__icontains="Martin").first()

if featured_instrument:
    print(f"Updating image for: {featured_instrument.brand} {featured_instrument.name}")

    # Download the image
    response = requests.get(image_url)
    if response.status_code == 200:
        # Save the image to the instrument
        image_name = "martin-d28-dreadnought.jpg"
        featured_instrument.image.save(image_name, File(BytesIO(response.content)), save=True)
        print(f"✓ Image updated successfully!")
        print(f"  Image saved as: {featured_instrument.image.url}")
    else:
        print(f"✗ Failed to download image. Status code: {response.status_code}")
else:
    print("✗ Martin Dreadnought not found")
