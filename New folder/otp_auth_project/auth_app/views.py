from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .serializers import RegistrationSerializer, LoginSerializer, VerifyOTPSerializer
from .models import User, OTP
from .utils import create_and_send_otp
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'success': True, 'message': 'User registered', 'user': {'id': user.id, 'email': user.email, 'mobile': user.mobile}}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')
        mobile = serializer.validated_data.get('mobile')

        user = None
        contact = None
        contact_type = None

        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'success': False, 'message': 'User with this email not found.'}, status=status.HTTP_404_NOT_FOUND)
            contact = email
            contact_type = OTP.CONTACT_EMAIL
        else:
            try:
                user = User.objects.get(mobile=mobile)
            except User.DoesNotExist:
                return Response({'success': False, 'message': 'User with this mobile not found.'}, status=status.HTTP_404_NOT_FOUND)
            contact = mobile
            contact_type = OTP.CONTACT_MOBILE

        otp = create_and_send_otp(contact, contact_type, user=user)

        return Response({'success': True, 'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)


class VerifyOTPAPIView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')
        mobile = serializer.validated_data.get('mobile')
        code = serializer.validated_data.get('code')

        if email:
            otps = OTP.objects.filter(contact=email, contact_type=OTP.CONTACT_EMAIL, code=code, is_used=False)
        else:
            otps = OTP.objects.filter(contact=mobile, contact_type=OTP.CONTACT_MOBILE, code=code, is_used=False)

        if not otps.exists():
            return Response({'success': False, 'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        otp = otps.order_by('-created_at').first()
        if otp.is_expired():
            return Response({'success': False, 'message': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        # mark used
        otp.mark_used()

        # generate JWT
        user = otp.user
        refresh = RefreshToken.for_user(user)
        return Response({'success': True, 'access': str(refresh.access_token), 'refresh': str(refresh)}, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'mobile': user.mobile,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return Response({'success': True, 'profile': data}, status=status.HTTP_200_OK)
