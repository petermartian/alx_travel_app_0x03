# listings/serializers.py
from rest_framework import serializers
from .models import Listing, Booking, Payment


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ["id", "title", "description", "price_per_night", "currency", "created_at"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "listing",
            "start_date",
            "end_date",
            "guests",
            "total_price",
            "currency",
            "created_at",
        ]
        read_only_fields = ["user", "created_at"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "booking",
            "tx_ref",
            "chapa_ref_id",
            "amount",
            "currency",
            "status",
            "checkout_url",
            "raw_init_resp",
            "raw_verify_resp",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["tx_ref", "status", "checkout_url", "raw_init_resp", "raw_verify_resp", "created_at", "updated_at"]
