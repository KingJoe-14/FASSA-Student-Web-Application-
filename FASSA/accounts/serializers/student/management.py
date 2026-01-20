from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class StudentManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'index_number', 'is_active']
