# listings/admin.py
from django.contrib import admin
from .models import Hotel, Booking, Payment


@admin.register(Hotel)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price_per_night", "currency", "created_at")
    search_fields = ("title",)
    list_filter = ("currency",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "start_date", "end_date", "guests", "total_price", "currency")
    search_fields = ("user__username", "listing__title")
    list_filter = ("currency", "start_date", "end_date")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "tx_ref", "status", "amount", "currency", "updated_at")
    search_fields = ("tx_ref", "booking__id")
    list_filter = ("status", "currency")
