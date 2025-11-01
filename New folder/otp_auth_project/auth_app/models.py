from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    # Allow register with email or mobile
    mobile = models.CharField(max_length=20, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.email or self.mobile or self.username


class OTP(models.Model):
    CONTACT_EMAIL = 'email'
    CONTACT_MOBILE = 'mobile'
    CONTACT_CHOICES = [
        (CONTACT_EMAIL, 'Email'),
        (CONTACT_MOBILE, 'Mobile'),
    ]

    user = models.ForeignKey('auth_app.User', on_delete=models.CASCADE, related_name='otps', null=True, blank=True)
    contact_type = models.CharField(max_length=10, choices=CONTACT_CHOICES)
    contact = models.CharField(max_length=255)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def mark_used(self):
        self.is_used = True
        self.save()

    def __str__(self):
        return f"OTP({self.contact} - {self.code})"
