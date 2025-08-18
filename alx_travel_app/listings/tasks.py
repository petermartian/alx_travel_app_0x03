from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Payment

@shared_task
def send_payment_receipt(payment_id: int):
    p = Payment.objects.select_related("booking", "booking__user").get(id=payment_id)
    user = p.booking.user
    subject = f"Payment confirmed for Booking #{p.booking.id}"
    body = f"Hi {user.get_full_name() or user.username},\n\nWe received your payment ({p.amount} {p.currency}).\nTx Ref: {p.tx_ref}\nStatus: {p.status}\n\nThanks!"
    to = [user.email] if user.email else []
    if to:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, to, fail_silently=True)
