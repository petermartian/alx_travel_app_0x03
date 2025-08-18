# listings/management/commands/seed_listings.py
from django.core.management.base import BaseCommand
from listings.models import Listing

SAMPLES = [
    dict(title="Lakeview Studio", description="Cozy by the lake", price_per_night=120, currency="USD"),
    dict(title="City Loft", description="Heart of downtown", price_per_night=185, currency="USD"),
]

class Command(BaseCommand):
    help = "Seed a few sample listings"

    def handle(self, *args, **kwargs):
        created = 0
        for data in SAMPLES:
            obj, was_created = Listing.objects.get_or_create(title=data["title"], defaults=data)
            created += 1 if was_created else 0
        self.stdout.write(self.style.SUCCESS(f"Seeded {created} new listing(s)."))
