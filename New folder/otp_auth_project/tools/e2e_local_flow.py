import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'otp_auth_project.settings')
import django
django.setup()

from auth_app.models import User, OTP
from auth_app.utils import create_and_send_otp
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

mobile = '9998887777'

print('1) Creating or getting user with mobile', mobile)
user, created = User.objects.get_or_create(username=mobile, defaults={'mobile': mobile, 'email': None})
if created:
    user.set_unusable_password()
    user.save()
    print('User created:', user.id)
else:
    print('User exists:', user.id)

print('\n2) Creating OTP using create_and_send_otp (will print SMS to console if SMS path used)')
otp = create_and_send_otp(mobile, contact_type=OTP.CONTACT_MOBILE, user=user)
print('OTP created:', otp.code, 'expires_at:', otp.expires_at)

print('\n3) Verifying OTP locally (ORM)')
if otp.is_expired():
    print('OTP has expired')
else:
    otp.mark_used()
    print('OTP marked used')

# Generate JWT
refresh = RefreshToken.for_user(user)
print('\n4) Generated tokens:')
print('access:', str(refresh.access_token))
print('refresh:', str(refresh))

print('\n5) Profile data:')
profile = {
    'id': user.id,
    'username': user.username,
    'email': user.email,
    'mobile': user.mobile,
    'first_name': user.first_name,
    'last_name': user.last_name,
}
print(profile)
