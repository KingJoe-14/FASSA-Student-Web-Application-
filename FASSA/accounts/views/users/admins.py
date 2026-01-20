from rest_framework import generics, filters
from ...serializers.admin.users import SuperAdminUserSerializer
from ...models import User
from ...permissions import IsSuperAdmin

class AdminListView(generics.ListAPIView):
    serializer_class = SuperAdminUserSerializer
    permission_classes = [IsSuperAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'email', 'position']

    def get_queryset(self):
        return User.objects.filter(role='ADMIN')


class AdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SuperAdminUserSerializer
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        return User.objects.filter(role='ADMIN')
