from celery import shared_task
from django.core.mail import send_mail
from .models import Booking

@shared_task
def send_booking_confirmation_email(booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        subject = f"Booking Confirmation for {booking.hotel.name}"
        message = f"Dear {booking.user.username},\n\nThank you for your booking at {booking.hotel.name}.\n\n"
        from_email = 'no-reply@alxtravelapp.com'
        recipient_list = [booking.user.email]
        send_mail(subject, message, from_email, recipient_list)
        return f"Confirmation email sent for booking ID {booking_id}"
    except Booking.DoesNotExist:
        return f"Booking with ID {booking_id} not found."
