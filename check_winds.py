import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daves_music_store.settings")
django.setup()

from store.models import Instrument

print("\nAll Wind Instruments:")
print("-" * 50)
winds = Instrument.objects.filter(category__name__icontains="Wind")
for wind in winds:
    print(f"{wind.brand} - {wind.name}")
