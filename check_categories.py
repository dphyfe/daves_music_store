import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daves_music_store.settings")
django.setup()

from store.models import Instrument, Category

print("\nAll Categories:")
print("-" * 50)
categories = Category.objects.all()
for cat in categories:
    print(f"{cat.name}")

print("\nAll Yamaha instruments:")
print("-" * 50)
yamahas = Instrument.objects.filter(brand__icontains="Yamaha")
for yamaha in yamahas:
    print(f"{yamaha.brand} - {yamaha.name} (Category: {yamaha.category.name})")
