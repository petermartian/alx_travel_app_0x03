from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

# Corrected imports to use Hotel instead of Listing
from .models import Hotel, Booking, Payment
from .serializers import HotelSerializer, BookingSerializer, PaymentSerializer
from .services import chapa

class HotelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows hotels to be viewed or edited.
    """
    queryset = Hotel.objects.all().order_by("-id")
    serializer_class = HotelSerializer
    permission_classes = [permissions.AllowAny]

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    """
    queryset = Booking.objects.all().order_by("-id")
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        # The serializer now saves the booking without payment logic
        serializer.save(user=self.request.user)


class InitiatePaymentAPIView(APIView):
    """
    Creates a Payment object for a booking and returns a Chapa checkout URL.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        booking_id = request.data.get("booking_id")
        currency = request.data.get("currency", "ETB")

        booking = get_object_or_404(Booking, id=booking_id)
        if booking.user != request.user:
            return Response({"detail": "You do not have permission to pay for this booking."}, status=status.HTTP_403_FORBIDDEN)

        # Use get_or_create to avoid creating duplicate payments for the same booking
        tx_ref = chapa.generate_tx_ref(prefix=f"booking-{booking.id}")
        payment, created = Payment.objects.get_or_create(
            booking=booking,
            defaults={
                "tx_ref": tx_ref,
                "amount": booking.total_price,
                "currency": currency,
                "status": Payment.Status.PENDING,
            }
        )

        # If payment already existed but failed, generate a new tx_ref
        if not created and payment.status == Payment.Status.FAILED:
            payment.tx_ref = tx_ref
            payment.status = Payment.Status.PENDING
            payment.save()

        user = request.user
        try:
            init_resp = chapa.initialize(
                amount=payment.amount,
                currency=payment.currency,
                email=user.email or "guest@example.com",
                first_name=user.first_name or "Guest",
                last_name=user.last_name or "User",
                tx_ref=payment.tx_ref,
                callback_url=getattr(settings, "API_CALLBACK_URL", None),
                return_url=getattr(settings, "FRONTEND_RETURN_URL", None),
                customization={"title": "Travel App Booking Payment"},
            )
            payment.raw_init_resp = init_resp
            payment.checkout_url = init_resp.get("data", {}).get("checkout_url", "")
            payment.save()
        except Exception as e:
            payment.status = Payment.Status.FAILED
            payment.raw_init_resp = {"error": str(e)}
            payment.save()
            return Response({"detail": "Payment provider could not be reached.", "error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        return Response({"checkout_url": payment.checkout_url}, status=status.HTTP_200_OK)


class VerifyPaymentAPIView(APIView):
    """
    Verifies a payment with Chapa using the transaction reference.
    This is typically used as the callback URL.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, tx_ref: str):
        payment = get_object_or_404(Payment, tx_ref=tx_ref)

        try:
            verify_resp = chapa.verify(tx_ref)
        except Exception as e:
            return Response({"detail": "Payment provider could not be reached.", "error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        payment.raw_verify_resp = verify_resp
        data = verify_resp.get("data", {})
        
        if data and data.get("status") == "success":
            payment.status = Payment.Status.COMPLETED
            payment.chapa_ref_id = data.get("reference") or data.get("ref_id") or ""
        else:
            payment.status = Payment.Status.FAILED

        payment.save()
        return Response(PaymentSerializer(payment).data, status=status.HTTP_200_OK)