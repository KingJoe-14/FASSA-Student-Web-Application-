from rest_framework import serializers
from clubs.models import Club, ClubMembership, ClubEvent
from accounts.models import User

# -------------------------------
# STUDENT SERIALIZER (nested for ClubMembership)
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
    student_email = serializers.EmailField(write_only=True)
    student = StudentSerializer(read_only=True)
    club = serializers.PrimaryKeyRelatedField(read_only=True)  # make read-only

    class Meta:
        model = ClubMembership
        fields = ['id', 'club', 'student', 'student_email', 'role', 'joined_at']
        read_only_fields = ['id', 'student', 'joined_at', 'club']

    def validate_student_email(self, email):
        try:
            user = User.objects.get(email=email, role='STUDENT')
        except User.DoesNotExist:
            raise serializers.ValidationError("Student with this email does not exist.")
        return user

    def create(self, validated_data):
        # Convert student_email into actual student object
        student = validated_data.pop('student_email')
        validated_data['student'] = student
        return super().create(validated_data)


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
