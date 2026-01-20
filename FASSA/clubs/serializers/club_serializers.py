from rest_framework import serializers
from clubs.models import Club

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'logo', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
