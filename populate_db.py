"""
Script to populate the database with sample musical instruments
Run this with: python populate_db.py
"""

import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daves_music_store.settings")
django.setup()

from store.models import Category, Instrument


def populate_database():
    print("Starting database population...")

    # Create Categories
    categories_data = [
        {"name": "Guitars", "slug": "guitars", "description": "Acoustic and electric guitars"},
        {"name": "Bass Guitars", "slug": "bass-guitars", "description": "Electric and acoustic bass guitars"},
        {"name": "Drums", "slug": "drums", "description": "Drum kits and percussion"},
        {"name": "Keyboards", "slug": "keyboards", "description": "Pianos, synthesizers, and keyboards"},
        {"name": "Wind Instruments", "slug": "wind-instruments", "description": "Saxophones, trumpets, flutes"},
        {"name": "String Instruments", "slug": "string-instruments", "description": "Violins, cellos, and violas"},
    ]

    categories = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(**cat_data)
        categories[cat_data["slug"]] = category
        print(f"{'Created' if created else 'Found'} category: {category.name}")

    # Create Instruments
    instruments_data = [
        {
            "name": "Stratocaster Electric Guitar",
            "slug": "fender-stratocaster",
            "category": categories["guitars"],
            "brand": "Fender",
            "condition": "new",
            "price": 1499.99,
            "rating": 4.8,
            "description": "Classic Fender Stratocaster with maple neck, alder body, and three single-coil pickups. Perfect for rock, blues, and pop.",
            "specifications": "- Body: Alder\n- Neck: Maple\n- Fretboard: Rosewood\n- Pickups: 3 Single-Coil\n- Bridge: Tremolo",
            "in_stock": True,
            "featured": True,
        },
        {
            "name": "Les Paul Standard",
            "slug": "gibson-les-paul",
            "category": categories["guitars"],
            "brand": "Gibson",
            "condition": "used_excellent",
            "price": 2299.99,
            "rating": 4.9,
            "description": "Iconic Gibson Les Paul with mahogany body and neck, rosewood fretboard. Incredible tone and sustain.",
            "specifications": "- Body: Mahogany\n- Top: Maple\n- Neck: Mahogany\n- Pickups: 2 Humbuckers\n- Finish: Sunburst",
            "in_stock": True,
            "featured": True,
        },
        {
            "name": "Precision Bass",
            "slug": "fender-precision-bass",
            "category": categories["bass-guitars"],
            "brand": "Fender",
            "condition": "new",
            "price": 1299.99,
            "rating": 4.7,
            "description": "The legendary Fender Precision Bass. Deep, punchy tone perfect for any genre.",
            "specifications": '- Body: Alder\n- Neck: Maple\n- Scale: 34"\n- Pickups: Split Single-Coil\n- Controls: Volume, Tone',
            "in_stock": True,
            "featured": True,
        },
        {
            "name": "Jazz Bass",
            "slug": "fender-jazz-bass",
            "category": categories["bass-guitars"],
            "brand": "Fender",
            "condition": "used_good",
            "price": 899.99,
            "rating": 4.5,
            "description": "Versatile Fender Jazz Bass with bright, articulate tone. Great for funk, jazz, and rock.",
            "specifications": "- Body: Alder\n- Neck: Maple\n- Pickups: 2 Single-Coil\n- Controls: 2 Volume, 1 Tone",
            "in_stock": True,
            "featured": False,
        },
        {
            "name": "5-Piece Drum Kit",
            "slug": "pearl-export-drum-kit",
            "category": categories["drums"],
            "brand": "Pearl",
            "condition": "new",
            "price": 799.99,
            "rating": 4.6,
            "description": "Complete Pearl Export 5-piece drum kit. Includes hardware and cymbals. Perfect for beginners and professionals.",
            "specifications": '- Bass Drum: 22"\n- Toms: 10", 12"\n- Floor Tom: 16"\n- Snare: 14"\n- Includes: Hi-hat, Crash, Ride cymbals',
            "in_stock": True,
            "featured": True,
        },
        {
            "name": "Digital Piano",
            "slug": "yamaha-p45",
            "category": categories["keyboards"],
            "brand": "Yamaha",
            "condition": "new",
            "price": 549.99,
            "rating": 4.4,
            "description": "Yamaha P-45 88-key weighted digital piano. Realistic feel and sound, perfect for home practice.",
            "specifications": "- Keys: 88 weighted\n- Voices: 10\n- Polyphony: 64-note\n- Built-in speakers\n- USB connectivity",
            "in_stock": True,
            "featured": True,
        },
        {
            "name": "Synthesizer",
            "slug": "korg-minilogue",
            "category": categories["keyboards"],
            "brand": "Korg",
            "condition": "used_excellent",
            "price": 499.99,
            "rating": 4.3,
            "description": "Korg Minilogue analog synthesizer with 4-voice polyphony. Great for electronic music production.",
            "specifications": "- Voices: 4\n- Keys: 37 slim keys\n- Oscillators: 2 per voice\n- Built-in sequencer\n- Multiple effects",
            "in_stock": True,
            "featured": False,
        },
        {
            "name": "Alto Saxophone",
            "slug": "yamaha-yas280",
            "category": categories["wind-instruments"],
            "brand": "Yamaha",
            "condition": "new",
            "price": 1999.99,
            "rating": 4.8,
            "description": "Yamaha YAS-280 student alto saxophone. Excellent tone quality and easy playability.",
            "specifications": "- Key: Eb\n- Finish: Gold lacquer\n- Includes: Hard case, mouthpiece, reeds\n- Perfect for students",
            "in_stock": True,
            "featured": True,
        },
        {
            "name": "Acoustic Dreadnought",
            "slug": "martin-d28",
            "category": categories["guitars"],
            "brand": "Martin",
            "condition": "used_excellent",
            "price": 2799.99,
            "rating": 4.9,
            "description": "Martin D-28 acoustic guitar with solid spruce top and rosewood back and sides. Rich, full sound.",
            "specifications": '- Top: Solid Spruce\n- Back/Sides: Rosewood\n- Neck: Mahogany\n- Scale: 25.4"\n- Includes: Hard case',
            "in_stock": True,
            "featured": False,
        },
        {
            "name": "Student Violin",
            "slug": "yamaha-v3ska",
            "category": categories["string-instruments"],
            "brand": "Yamaha",
            "condition": "new",
            "price": 329.99,
            "rating": 4.2,
            "description": "Yamaha V3 SKA 4/4 student violin outfit. Great quality for beginners.",
            "specifications": "- Size: 4/4\n- Top: Spruce\n- Back/Sides: Maple\n- Includes: Case, bow, rosin",
            "in_stock": True,
            "featured": False,
        },
        {
            "name": "Classical Guitar",
            "slug": "cordoba-c5",
            "category": categories["guitars"],
            "brand": "Cordoba",
            "condition": "new",
            "price": 399.99,
            "rating": 4.6,
            "description": "Cordoba C5 classical guitar with cedar top and mahogany back and sides. Warm, mellow tone.",
            "specifications": "- Top: Canadian Cedar\n- Back/Sides: Mahogany\n- Neck: Mahogany\n- Fretboard: Rosewood\n- Nylon strings",
            "in_stock": True,
            "featured": False,
        },
    ]

    for inst_data in instruments_data:
        instrument, created = Instrument.objects.update_or_create(slug=inst_data["slug"], defaults=inst_data)
        print(f"{'Created' if created else 'Updated'} instrument: {instrument.brand} {instrument.name}")

    print("\nDatabase population complete!")
    print(f"Total categories: {Category.objects.count()}")
    print(f"Total instruments: {Instrument.objects.count()}")
    print("\nYou can now view the store at: http://127.0.0.1:8000/")
    print("Admin panel at: http://127.0.0.1:8000/admin/")


if __name__ == "__main__":
    populate_database()
