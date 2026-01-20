from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdmin, IsSuperAdmin
from clubs.models import Club
from clubs.serializers import ClubSerializer


class AdminClubListCreateView(generics.ListCreateAPIView):
    """List all clubs or create a new club (Admin/Superadmin)"""
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = Club.objects.all().order_by('-created_at')


class AdminClubRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a club"""
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = Club.objects.all()
