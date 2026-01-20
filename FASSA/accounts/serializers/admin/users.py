from rest_framework import serializers
from django.contrib.auth import get_user_model

from ...utils import generate_temporary_password, send_account_email

User = get_user_model()


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
                raise serializers.ValidationError({"index_number": "Index number is required."})
            if position:
                raise serializers.ValidationError({"position": "Students should not have a position."})

        elif role == 'ADMIN':
            if not position:
                raise serializers.ValidationError({"position": "Admins require a position."})
            if index_number:
                raise serializers.ValidationError({"index_number": "Admins cannot have index numbers."})

        return attrs

    def create(self, validated_data):
        temp_password = generate_temporary_password()

        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            role=validated_data['role'],
            index_number=validated_data.get('index_number'),
            position=validated_data.get('position'),
            password=temp_password
        )

        send_account_email(
            user.email,
            user.full_name,
            user.role,
            temp_password
        )

        return user
