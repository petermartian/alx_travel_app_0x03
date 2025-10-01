# listings/views.py
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer
from .services import chapa


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all().order_by("-id")
    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by("-id")
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)

        # Default to ETB for sandbox to avoid currency restrictions
        currency = (booking.currency or "ETB") or "ETB"

        tx_ref = chapa.generate_tx_ref(prefix=f"booking-{booking.id}")
        payment = Payment.objects.create(
            booking=booking,
            tx_ref=tx_ref,
            amount=booking.total_price,
            currency=currency,
            status=Payment.Status.PENDING,
        )

        email = getattr(self.request.user, "email", "") or "guest@example.com"
        first_name = getattr(self.request.user, "first_name", "") or ""
        last_name = getattr(self.request.user, "last_name", "") or ""

        try:
            init_resp = chapa.initialize(
                amount=booking.total_price,
                currency=currency,
                email=email,
                first_name=first_name,
                last_name=last_name,
                tx_ref=tx_ref,
                callback_url=getattr(settings, "API_CALLBACK_URL", None) or None,
                return_url=getattr(settings, "FRONTEND_RETURN_URL", None) or None,
                customization={"title": "Booking Payment", "description": f"Booking #{booking.id}"},
                meta={"booking_id": booking.id},
            )
            payment.raw_init_resp = init_resp
            payment.checkout_url = (init_resp.get("data") or {}).get("checkout_url", "")
            payment.save(update_fields=["raw_init_resp", "checkout_url"])
            self._checkout_url = payment.checkout_url
        except Exception as e:
            payment.status = Payment.Status.FAILED
            payment.raw_init_resp = {"error": str(e)}
            payment.save(update_fields=["status", "raw_init_resp"])
            self._checkout_url = None

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        resp.data["checkout_url"] = getattr(self, "_checkout_url", None)
        return resp


class InitiatePaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Body: { "booking_id": <id>, "currency": "ETB" }
        """
        booking_id = request.data.get("booking_id")
        # Default to ETB for sandbox (can override with USD if your account supports it)
        currency = request.data.get("currency") or "ETB"

        booking = get_object_or_404(Booking, id=booking_id)
        if booking.user != request.user:
            return Response({"detail": "Forbidden"}, status=403)

        payment = getattr(booking, "payment", None)
        if not payment:
            tx_ref = chapa.generate_tx_ref(prefix=f"booking-{booking.id}")
            payment = Payment.objects.create(
                booking=booking,
                tx_ref=tx_ref,
                amount=booking.total_price,
                currency=currency,
                status=Payment.Status.PENDING,
            )

        email = getattr(request.user, "email", "") or "guest@example.com"
        first_name = getattr(request.user, "first_name", "") or ""
        last_name = getattr(request.user, "last_name", "") or ""

        try:
            init_resp = chapa.initialize(
                amount=payment.amount,
                currency=payment.currency or currency,
                email=email,
                first_name=first_name,
                last_name=last_name,
                tx_ref=payment.tx_ref,
                callback_url=getattr(settings, "API_CALLBACK_URL", None) or None,
                return_url=getattr(settings, "FRONTEND_RETURN_URL", None) or None,
                customization={"title": "Booking Payment", "description": f"Booking #{booking.id}"},
                meta={"booking_id": booking.id},
            )
            payment.raw_init_resp = init_resp
            payment.checkout_url = (init_resp.get("data") or {}).get("checkout_url", "")
            payment.save(update_fields=["raw_init_resp", "checkout_url"])
        except Exception as e:
            payment.status = Payment.Status.FAILED
            payment.raw_init_resp = {"error": str(e)}
            payment.save(update_fields=["status", "raw_init_resp"])
            return Response({"detail": "Chapa init failed", "error": str(e)}, status=502)

        return Response({"payment": PaymentSerializer(payment).data, "checkout_url": payment.checkout_url}, status=201)


class VerifyPaymentAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, tx_ref: str):
        payment = get_object_or_404(Payment, tx_ref=tx_ref)

        try:
            verify_resp = chapa.verify(tx_ref)
        except Exception as e:
            return Response({"detail": "Chapa verify failed", "error": str(e)}, status=502)

        payment.raw_verify_resp = verify_resp
        status_value = (verify_resp.get("status") or "").lower()
        data_status = ((verify_resp.get("data") or {}).get("status") or "").lower()
        final = data_status or status_value

        if final == "success":
            payment.status = Payment.Status.COMPLETED
            payment.chapa_ref_id = (verify_resp.get("data") or {}).get("reference") or \
                                   (verify_resp.get("data") or {}).get("ref_id") or ""
        else:
            payment.status = Payment.Status.FAILED

        payment.save(update_fields=["status", "raw_verify_resp", "chapa_ref_id"])
        return Response(PaymentSerializer(payment).data, status=200)


# Optional aliases
InitiatePaymentView = InitiatePaymentAPIView
VerifyPaymentView = VerifyPaymentAPIView
