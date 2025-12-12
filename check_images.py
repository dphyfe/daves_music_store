import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daves_music_store.settings")
django.setup()

from store.models import Instrument

instruments = Instrument.objects.filter(featured=True, in_stock=True).order_by("?")[:8]
print(f"Featured instruments count: {len(instruments)}\n")

for i in instruments:
    print(f"{i.brand} {i.name}")
    print(f"  Image field: {i.image}")
    print(f"  Image URL: {i.image_display_url or 'No image'}")
    print(f"  Has image: {bool(i.image)}")
    print()
