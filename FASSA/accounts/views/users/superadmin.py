from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from ...serializers.admin.users import SuperAdminUserSerializer
from ...models import User
from ...permissions import IsSuperAdmin, IsAdmin

class SuperAdminUserView(generics.ListCreateAPIView):
    serializer_class = SuperAdminUserSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]
    queryset = User.objects.all()

    def perform_create(self, serializer):
        current = self.request.user
        role = serializer.validated_data.get("role")

        if current.role == "SUPERADMIN":
            serializer.save()
        elif current.role == "ADMIN" and role == "STUDENT":
            serializer.save()
        else:
            raise PermissionDenied("You cannot create this type of account.")
