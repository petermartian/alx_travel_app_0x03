from rest_framework import serializers
from .models import Hotel, Booking, Payment

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ["id", "name", "location", "price_per_night"]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "user", "hotel", "check_in_date", "check_out_date", "num_guests"]
        read_only_fields = ["user"]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["tx_ref", "status", "created_at", "updated_at"]