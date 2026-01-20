from rest_framework import generics, filters, permissions
from rest_framework.response import Response
from ...serializers.student.registration import StudentRegistrationSerializer
from ...serializers.student.management import StudentManagementSerializer
from ...models import User
from ...permissions import IsAdmin, IsSuperAdmin

class StudentRegisterView(generics.CreateAPIView):
    serializer_class = StudentRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class StudentListView(generics.ListAPIView):
    serializer_class = StudentManagementSerializer
    permission_classes = [IsAdmin | IsSuperAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'email', 'index_number']

    def get_queryset(self):
        return User.objects.filter(role='STUDENT')


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentManagementSerializer
    permission_classes = [IsAdmin | IsSuperAdmin]

    def get_queryset(self):
        return User.objects.filter(role='STUDENT')
