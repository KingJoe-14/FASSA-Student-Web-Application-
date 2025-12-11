from datetime import timedelta
import uuid
import random

from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status, filters, permissions
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import AccountVerificationOTP, User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import PasswordResetOTP
from .serializers import (
    StudentRegistrationSerializer,
    SuperAdminUserSerializer,
    LoginSerializer,
    UserProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    StudentManagementSerializer,
)
from .permissions import IsSuperAdmin, IsAdmin, IsStudent
from .utils import send_password_reset_otp


User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful.",
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class StudentRegisterView(generics.CreateAPIView):
    serializer_class = StudentRegistrationSerializer
    permission_classes = [AllowAny]

class VerifyStudentAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if OTP record exists
        try:
            record = AccountVerificationOTP.objects.get(email=email, otp=otp)
        except AccountVerificationOTP.DoesNotExist:
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email)

        # If already verified
        if user.is_verified:
            return Response({"message": "Account already verified."}, status=status.HTTP_200_OK)

        # Verify & activate account
        user.is_verified = True
        user.is_active = True
        user.save()

        # Delete OTP record after successful verification
        record.delete()

        return Response({"message": "Account verified successfully."}, status=status.HTTP_200_OK)


class SuperAdminUserView(generics.ListCreateAPIView):
    serializer_class = SuperAdminUserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def perform_create(self, serializer):
        current_user = self.request.user
        role = serializer.validated_data.get("role")

        if current_user.role == "SUPERADMIN":
            serializer.save()
        elif current_user.role == "ADMIN":
            if role != "STUDENT":
                raise PermissionDenied("Admins can only create student accounts.")
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to create accounts.")


class StudentListView(generics.ListAPIView):
    serializer_class = StudentManagementSerializer
    permission_classes = [IsAdmin | IsSuperAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'email', 'index_number']

    def get_queryset(self):
        return User.objects.filter(role='STUDENT')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "count": queryset.count(),
            "students": serializer.data
        })


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentManagementSerializer
    permission_classes = [IsAdmin | IsSuperAdmin]

    def get_queryset(self):
        return User.objects.filter(role='STUDENT')


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Do not reveal whether email exists
            return Response({"detail": "If this email exists, an OTP will be sent."}, status=status.HTTP_200_OK)

        otp_code = PasswordResetOTP.generate_otp()
        PasswordResetOTP.objects.create(email=user.email, otp=otp_code)
        send_password_reset_otp(user.email, otp_code)

        return Response({"detail": "A code has been sent to your inbox, use it to reset your password."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']

        reset_obj = get_object_or_404(PasswordResetOTP, email=email, otp=otp)

        if reset_obj.is_expired():
            return Response({"detail": "OTP expired."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email)
        user.set_password(new_password)
        user.save()
        reset_obj.delete()

        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)

class AdminListView(generics.ListAPIView):
    serializer_class = SuperAdminUserSerializer
    permission_classes = [IsSuperAdmin]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'email', 'position']

    def get_queryset(self):
        return User.objects.filter(role='ADMIN')

class AdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SuperAdminUserSerializer
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        return User.objects.filter(role='ADMIN')
