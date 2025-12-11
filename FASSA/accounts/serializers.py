from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .utils import (
    generate_temporary_password,
    send_account_email,
    send_student_verification_otp,
)
from .models import AccountVerificationOTP


User = get_user_model()


class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'index_number', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            index_number=validated_data['index_number'],
            role='STUDENT',
            password=validated_data['password'],
            is_active=False,  # inactive until verified
            is_verified=False  # custom field for verification
        )

        # --- Generate OTP for verification ---
        otp_code = AccountVerificationOTP.generate_otp()

        # Save OTP in the database
        AccountVerificationOTP.objects.create(
            email=user.email,
            otp=otp_code
        )

        # Send email to user
        send_student_verification_otp(
            email=user.email,
            full_name=user.full_name,
            otp=otp_code
        )

        return user


class SuperAdminUserSerializer(serializers.ModelSerializer):
    index_number = serializers.CharField(required=False, allow_blank=True)
    position = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=[('STUDENT', 'Student'), ('ADMIN', 'Admin')])

    class Meta:
        model = User
        fields = ['full_name', 'email', 'role', 'index_number', 'position']

    def validate(self, attrs):
        role = attrs.get('role')
        index_number = attrs.get('index_number')
        position = attrs.get('position')

        if role == 'STUDENT':
            if not index_number:
                raise serializers.ValidationError({"index_number": "Index number is required for student accounts."})
            if position:
                raise serializers.ValidationError({"position": "Students should not have a position field."})

        elif role == 'ADMIN':
            if not position:
                raise serializers.ValidationError({"position": "Position is required for admin accounts."})
            if index_number:
                raise serializers.ValidationError({"index_number": "Admins should not have an index number."})

        return attrs

    def create(self, validated_data):
        temp_password = generate_temporary_password()
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            role=validated_data['role'],
            index_number=validated_data.get('index_number'),
            position=validated_data.get('position'),
            password=temp_password,
        )

        send_account_email(
            user_email=user.email,
            full_name=user.full_name,
            role=user.role,
            temp_password=temp_password,
        )

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'role', 'index_number', 'position', 'is_active']


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs


class StudentManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'index_number', 'is_active']

