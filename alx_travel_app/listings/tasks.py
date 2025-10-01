from celery import shared_task
from django.core.mail import send_mail
from .models import Booking

@shared_task
def send_booking_confirmation_email(booking_id):
    """
    Celery task to send a booking confirmation email asynchronously.
    """
    try:
        booking = Booking.objects.get(id=booking_id)
        subject = f"Booking Confirmation for {booking.hotel.name}"
        message = (
            f"Dear {booking.user.username},\n\n"
            f"Thank you for your booking at {booking.hotel.name}.\n\n"
            f"Booking Details:\n"
            f"- Check-in: {booking.check_in_date}\n"
            f"- Check-out: {booking.check_out_date}\n"
            f"- Guests: {booking.num_guests}\n\n"
            f"We look forward to welcoming you!\n\n"
            f"Best regards,\nThe ALX Travel App Team"
        )
        from_email = 'no-reply@alxtravelapp.com'
        recipient_list = [booking.user.email]

        send_mail(subject, message, from_email, recipient_list)
        return f"Confirmation email sent for booking ID {booking_id}"
    except Booking.DoesNotExist:
        return f"Booking with ID {booking_id} not found."