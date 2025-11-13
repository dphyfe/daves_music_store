import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daves_music_store.settings")
django.setup()

from store.models import Instrument

print("\nAll Keyboard instruments:")
print("-" * 50)
keyboards = Instrument.objects.filter(category__name__icontains="Keyboard")
for keyboard in keyboards:
    print(f"{keyboard.brand} - {keyboard.name}")
