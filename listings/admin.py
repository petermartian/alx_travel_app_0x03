from django.contrib import admin
from .models import Hotel, Booking, Payment

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location", "price_per_night")
    search_fields = ("name", "location")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "hotel", "check_in_date", "check_out_date")
    search_fields = ("user__username", "hotel__name")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "tx_ref", "status", "amount", "updated_at")
    search_fields = ("tx_ref", "booking__id")
    list_filter = ("status",)