import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daves_music_store.settings")
django.setup()

from store.models import Instrument

print("\nAll Horn instruments:")
print("-" * 50)
horns = Instrument.objects.filter(category__name__icontains="Horn")
for horn in horns:
    print(f"{horn.brand} - {horn.name}")
