import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'otp_auth_project.settings')
import django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = os.getenv('SUPERUSER_USERNAME', 'admin')
EMAIL = os.getenv('SUPERUSER_EMAIL', 'admin@example.com')
PASSWORD = os.getenv('SUPERUSER_PASSWORD', 'AdminPass123!')

if User.objects.filter(username=USERNAME).exists():
    print(f"Superuser '{USERNAME}' already exists.")
else:
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print(f"Created superuser: username={USERNAME}, email={EMAIL}")
