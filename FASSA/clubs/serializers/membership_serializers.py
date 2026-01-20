from rest_framework import serializers
from accounts.models import User
from clubs.models import ClubMembership

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']

class ClubMembershipSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='STUDENT'),
        write_only=True
    )

    class Meta:
        model = ClubMembership
        fields = [
            'id', 'club', 'student', 'student_id',
            'role', 'executive_photo', 'executive_title', 'joined_at'
        ]
        read_only_fields = ['id', 'joined_at', 'student', 'club']

    def create(self, validated_data):
        student = validated_data.pop('student_id')
        club = self.context['club']
        return ClubMembership.objects.create(student=student, club=club, **validated_data)
