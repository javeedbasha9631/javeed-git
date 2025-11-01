from rest_framework import serializers
from .models import User, OTP
from django.utils import timezone


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True)
    mobile = serializers.CharField(required=False, allow_null=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        email = data.get('email')
        mobile = data.get('mobile')
        if not email and not mobile:
            raise serializers.ValidationError('Provide either email or mobile for registration.')
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exists.')
        if mobile and User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError('User with this mobile already exists.')
        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        mobile = validated_data.get('mobile')
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')

        username = email or mobile
        user = User.objects.create_user(username=username, email=email or None, password=None)
        user.first_name = first_name
        user.last_name = last_name
        if mobile:
            user.mobile = mobile
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False)

    def validate(self, data):
        if not data.get('email') and not data.get('mobile'):
            raise serializers.ValidationError('Provide email or mobile to login.')
        return data


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False)
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        if not data.get('email') and not data.get('mobile'):
            raise serializers.ValidationError('Provide email or mobile plus code.')
        return data
