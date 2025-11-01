from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTP


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Extra", {'fields': ('mobile',)}),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('contact', 'code', 'contact_type', 'user', 'is_used', 'created_at', 'expires_at')
    list_filter = ('contact_type', 'is_used')
    readonly_fields = ('created_at',)
