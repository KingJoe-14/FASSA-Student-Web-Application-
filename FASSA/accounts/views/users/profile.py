from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ...serializers.profile.profile import UserProfileSerializer

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
