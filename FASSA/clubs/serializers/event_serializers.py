from rest_framework import serializers
from clubs.models import ClubEvent

class ClubEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubEvent
        fields = [
            'id', 'club', 'title', 'description', 'venue',
            'event_date', 'is_approved', 'created_by', 'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

class ClubEventApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubEvent
        fields = ['is_approved']
