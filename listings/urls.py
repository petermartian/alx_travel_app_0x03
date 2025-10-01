from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    HotelViewSet,
    BookingViewSet,
    InitiatePaymentAPIView,
    VerifyPaymentAPIView,
)

router = DefaultRouter()
router.register(r"hotels", HotelViewSet, basename="hotel")
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("", include(router.urls)),
    path("payments/initiate/", InitiatePaymentAPIView.as_view(), name="payments-initiate"),
    path("payments/verify/<str:tx_ref>/", VerifyPaymentAPIView.as_view(), name="payments-verify"),
]