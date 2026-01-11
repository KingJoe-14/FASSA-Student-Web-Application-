from rest_framework import serializers
from clubs.models import Club, ClubMembership, ClubEvent
from accounts.models import User

# -------------------------------
# STUDENT SERIALIZER (nested output)
# -------------------------------
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']


# -------------------------------
# CLUB SERIALIZER
# -------------------------------
class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'name', 'description', 'logo', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


# -------------------------------
# CLUB MEMBERSHIP SERIALIZER
# -------------------------------
class ClubMembershipSerializer(serializers.ModelSerializer):
    # Nested output
    student = StudentSerializer(read_only=True)
    club = ClubSerializer(read_only=True)

    # Input only
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='STUDENT'),
        write_only=True
    )

    role = serializers.ChoiceField(
        choices=ClubMembership.ROLE_CHOICES,
        default='MEMBER'
    )

    class Meta:
        model = ClubMembership
        fields = [
            'id',
            'club',
            'student',
            'student_id',
            'role',
            'executive_photo',
            'executive_title',
            'joined_at'
        ]
        read_only_fields = ['id', 'joined_at', 'student', 'club']

    def validate(self, attrs):
        role = attrs.get('role', 'MEMBER')

        executive_roles = [
            'PRESIDENT',
            'VICE_PRESIDENT',
            'SECRETARY',
            'TREASURER'
        ]

        if role in executive_roles:
            if not attrs.get('executive_photo'):
                raise serializers.ValidationError(
                    {"executive_photo": "Executive photo is required."}
                )

        return attrs

    def create(self, validated_data):
        student = validated_data.pop('student_id')
        club = self.context['club']

        return ClubMembership.objects.create(
            student=student,
            club=club,
            **validated_data
        )


# -------------------------------
# CLUB EVENT SERIALIZER
# -------------------------------
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

