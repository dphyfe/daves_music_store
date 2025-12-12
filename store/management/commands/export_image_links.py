from django.core.management.base import BaseCommand
from django.conf import settings
import csv
from store.models import Instrument


class Command(BaseCommand):
    help = "Export instrument image links to CSV"

    def add_arguments(self, parser):
        parser.add_argument("--output", "-o", default="image_links.csv", help="Output CSV path")
        parser.add_argument(
            "--base-url",
            "-b",
            default="",
            help="Optional base URL to prefix to media paths (e.g. https://example.com)",
        )

    def handle(self, *args, **options):
        out_path = options["output"]
        base_url = options["base_url"].rstrip("/")

        with open(out_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["id", "name", "slug", "image_link"])

            for inst in Instrument.objects.all():
                img_name = inst.image.name if inst.image else ""
                if img_name:
                    media_url = settings.MEDIA_URL or ""
                    if not media_url.startswith("/"):
                        media_url = "/" + media_url
                    media_url = media_url.rstrip("/")
                    link = f"{media_url}/{img_name}"
                    if base_url:
                        link = base_url + link
                else:
                    link = ""

                writer.writerow([inst.id, inst.name, inst.slug, link])

        self.stdout.write(self.style.SUCCESS(f"Wrote image links to {out_path}"))
