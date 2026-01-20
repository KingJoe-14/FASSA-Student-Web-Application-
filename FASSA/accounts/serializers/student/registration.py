from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from ...models import AccountVerificationOTP
from ...utils import send_student_verification_otp

User = get_user_model()


class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

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
            is_active=False,
            is_verified=False
        )

        otp_code = AccountVerificationOTP.generate_otp()
        AccountVerificationOTP.objects.create(email=user.email, otp=otp_code)

        send_student_verification_otp(user.email, user.full_name, otp_code)

        return user
