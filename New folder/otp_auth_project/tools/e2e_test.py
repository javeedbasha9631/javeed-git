import os
import sys
import time
import json

# Use the project's python path if necessary
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Configure Django environment to access ORM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'otp_auth_project.settings')
import django
django.setup()

from django.utils import timezone
from auth_app.models import OTP, User

import requests

BASE_URL = 'http://127.0.0.1:8000'

# Test data
mobile = '9998887777'

print('1) Registering user with mobile:', mobile)
resp = requests.post(f'{BASE_URL}/register/', json={'mobile': mobile})
print('Register response:', resp.status_code, resp.text)

print('\n2) Requesting OTP via /login/')
resp = requests.post(f'{BASE_URL}/login/', json={'mobile': mobile})
print('Login response:', resp.status_code, resp.text)

# Wait briefly to ensure OTP created
time.sleep(1)

# Fetch latest OTP from DB for this mobile
print('\n3) Reading latest OTP from DB (for test purposes)')
otps = OTP.objects.filter(contact=mobile, contact_type=OTP.CONTACT_MOBILE).order_by('-created_at')
if not otps.exists():
    print('No OTP found in DB for mobile', mobile)
    sys.exit(1)

otp = otps.first()
print('Found OTP:', otp.code, 'created_at:', otp.created_at, 'expires_at:', otp.expires_at)

# Verify OTP
print('\n4) Verifying OTP via /verify-otp/')
resp = requests.post(f'{BASE_URL}/verify-otp/', json={'mobile': mobile, 'code': otp.code})
print('Verify response:', resp.status_code, resp.text)

if resp.status_code != 200:
    print('OTP verification failed; aborting')
    sys.exit(1)

data = resp.json()
access = data.get('access')
refresh = data.get('refresh')
print('\nReceived tokens: access length=', len(access) if access else None)

# Call protected profile
print('\n5) Calling protected /profile/ with access token')
headers = {'Authorization': f'Bearer {access}'}
resp = requests.get(f'{BASE_URL}/profile/', headers=headers)
print('Profile response:', resp.status_code, resp.text)

print('\nEnd-to-end test complete.')
