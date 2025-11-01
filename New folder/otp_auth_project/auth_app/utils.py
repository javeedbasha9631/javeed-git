import random
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail

from .models import OTP


def generate_otp_code(length=6):
    return ''.join(random.choices('0123456789', k=length))


def send_otp_email(email, code):
    subject = 'Your OTP Code'
    message = f'Your one-time password (OTP) is: {code}. It will expire in 2 minutes.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def send_otp_sms(mobile, code):
    # Placeholder for SMS sending. For now, we just log to console.
    # In production integrate with Twilio or other SMS provider.
    print(f"Sending SMS to {mobile}: Your OTP is {code}")


def create_and_send_otp(contact, contact_type='email', user=None):
    code = generate_otp_code(6)
    expires_at = timezone.now() + timedelta(minutes=2)

    otp = OTP.objects.create(
        user=user,
        contact_type=contact_type,
        contact=contact,
        code=code,
        expires_at=expires_at,
    )

    # Send via appropriate channel
    if contact_type == OTP.CONTACT_EMAIL:
        try:
            send_otp_email(contact, code)
        except Exception as e:
            # For local dev, you might use console email backend; bubble up otherwise
            print('Failed to send email:', e)
    else:
        send_otp_sms(contact, code)

    return otp
