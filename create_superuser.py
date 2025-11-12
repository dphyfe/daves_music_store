"""
Quick script to create a superuser for the admin panel
Username: admin
Password: admin123
Email: admin@davesworldofmusic.com
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daves_music_store.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "admin"
email = "admin@davesworldofmusic.com"
password = "admin123"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser created successfully!")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"\nYou can now login at: http://127.0.0.1:8000/admin/")
else:
    print(f"Superuser '{username}' already exists.")
    print(f"\nLogin at: http://127.0.0.1:8000/admin/")
    print(f"Username: {username}")
    print(f"Password: {password}")
