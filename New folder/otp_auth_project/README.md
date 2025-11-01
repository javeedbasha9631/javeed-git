OTP-based Authentication System (Django + DRF)

Overview

This project demonstrates an OTP (one-time password) based login flow using Django and Django REST Framework. OTPs are sent to a user's email or mobile and expire after 2 minutes. After successful OTP verification, a JWT access token is issued.

Features

- Register with email or mobile (/register/)
- Request OTP to email or mobile (/login/)
- Verify OTP and get JWT (/verify-otp/)
- Protected profile route (/profile/) that requires Bearer JWT

Quick start

1. Clone or copy the project into a folder.
2. Create a virtual environment and activate it.

# Windows (PowerShell)
python -m venv .venv; .\.venv\Scripts\Activate.ps1

3. Install dependencies:

pip install -r requirements.txt

4. Copy `.env.example` to `.env` and update values. For local development you can use the console email backend by setting:

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

This will print OTP emails to the console instead of sending real emails.

5. Run migrations:

python manage.py migrate

6. (Optional) Create a superuser:

python manage.py createsuperuser

7. Run the development server:

python manage.py runserver

8. Open http://127.0.0.1:8000/home/ to use the simple frontend, or call the API endpoints directly:

- POST /register/  {"email": "..."} or {"mobile": "..."}
- POST /login/     {"email": "..."} or {"mobile": "..."}
- POST /verify-otp/ {"email": "...", "code": "123456"}
- GET /profile/    (requires Authorization: Bearer <access_token>)

Notes and environment

- Uses SQLite (db.sqlite3) by default.
- JWT tokens are provided by djangorestframework-simplejwt.
- For SMS sending, the implementation currently prints to console (placeholder). Integrate with Twilio or similar for real SMS.

Files of interest

- `auth_app/models.py` - User and OTP models
- `auth_app/utils.py` - OTP generation and send helpers
- `auth_app/serializers.py` - DRF serializers for register/login/verify
- `auth_app/views.py` - API views
- `auth_app/urls.py` - API routing
- `auth_app/templates/index.html` - Simple frontend

Security

- Keep `.env` out of version control and never commit real credentials.
- Set a strong `SECRET_KEY` and disable DEBUG in production.

That's it — you should now have a working OTP-auth demo. If you want, I can run quick checks (migrations, start server) or add tests next.
