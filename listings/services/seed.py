from django.core.management.base import BaseCommand
from listings.models import Listing

class Command(BaseCommand):
    help = "Seed the database with sample listings"

    def handle(self, *args, **options):
        # Optional: wipe out old data
        Listing.objects.all().delete()

        sample_listings = [
            {
                "title": "Cozy Mountain Cabin",
                "description": "A quiet retreat nestled in the Rockies.",
                "location": "Aspen, CO",
                "price": 150.00,
                "available": True,
            },
            {
                "title": "Beachfront Bungalow",
                "description": "Enjoy sunrise views over the Pacific.",
                "location": "Santa Monica, CA",
                "price": 225.00,
                "available": True,
            },
            {
                "title": "Urban Loft Apartment",
                "description": "Modern loft in the heart of downtown.",
                "location": "New York, NY",
                "price": 300.00,
                "available": False,
            },
            {
                "title": "Countryside Villa",
                "description": "Sprawling estate with pool and gardens.",
                "location": "Tuscany, Italy",
                "price": 450.00,
                "available": True,
            },
            {
                "title": "Lake House Retreat",
                "description": "Perfect getaway on the shores of Lake Tahoe.",
                "location": "South Lake Tahoe, CA",
                "price": 200.00,
                "available": True,
            },
        ]

        for data in sample_listings:
            Listing.objects.create(**data)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(sample_listings)} listings."
        ))
