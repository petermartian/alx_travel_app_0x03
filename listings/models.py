from django.db import models
from django.conf import settings
from datetime import date

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.PositiveIntegerField()

    @property
    def total_price(self):
        """Calculates the total price for the booking."""
        if self.check_in_date and self.check_out_date and self.check_in_date < self.check_out_date:
            num_nights = (self.check_out_date - self.check_in_date).days
            return self.hotel.price_per_night * num_nights
        return 0

    def __str__(self):
        return f"Booking for {self.hotel.name} by {self.user.username}"

class Payment(models.Model):
    # --- Add Status choices ---
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    tx_ref = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="ETB") # <-- Add currency field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Add fields to store Chapa's responses
    raw_init_resp = models.JSONField(default=dict)
    raw_verify_resp = models.JSONField(default=dict)
    checkout_url = models.URLField(blank=True, null=True)
    chapa_ref_id = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"Payment for Booking #{self.booking.id} - Status: {self.status}"