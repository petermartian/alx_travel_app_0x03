# listings/tests/test_smoke.py
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from listings.models import Listing, Booking

User = get_user_model()

def create_user(username="u1", password="pass123", email="u1@example.com"):
    return User.objects.create_user(username=username, password=password, email=email)

def test_listings_list_ok(db):
    Listing.objects.create(title="Test A", price_per_night=100)
    client = APIClient()
    url = reverse("listing-list")  # from DefaultRouter in listings/urls.py
    resp = client.get(url)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_payments_initiate_requires_auth(db):
    user = create_user()
    l = Listing.objects.create(title="Test B", price_per_night=100)
    booking = Booking.objects.create(
        user=user, listing=l, start_date="2025-08-20", end_date="2025-08-21",
        guests=1, total_price=100, currency="ETB"
    )
    client = APIClient()  # not authenticated
    url = reverse("payments-initiate")
    resp = client.post(url, {"booking_id": booking.id, "currency": "ETB"}, format="json")
    # IsAuthenticated on the view should reject anonymous
    assert resp.status_code in (401, 403)
