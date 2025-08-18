# listings/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone


class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default="USD")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.title} ({self.currency} {self.price_per_night})"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    # For simplicity we store a computed total here (e.g., nights * price_per_night)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Booking #{self.id} - {self.user} - {self.listing}"


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"
        CANCELED = "CANCELED", "Canceled"

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    tx_ref = models.CharField(max_length=80, unique=True)
    chapa_ref_id = models.CharField(max_length=80, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    checkout_url = models.URLField(blank=True)
    raw_init_resp = models.JSONField(default=dict, blank=True)
    raw_verify_resp = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.tx_ref} [{self.status}]"
