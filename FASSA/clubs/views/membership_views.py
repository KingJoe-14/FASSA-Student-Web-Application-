from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdmin, IsSuperAdmin
from clubs.models import Club, ClubMembership
from clubs.serializers import ClubMembershipSerializer


class AdminClubMemberListCreateView(generics.ListCreateAPIView):
    """List members of a club or add a new member (Admin/Superadmin)"""
    serializer_class = ClubMembershipSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]

    def get_queryset(self):
        return ClubMembership.objects.filter(club_id=self.kwargs['club_id'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['club'] = get_object_or_404(Club, id=self.kwargs['club_id'])
        return context


class AdminClubMemberRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update (role), or remove a member from a club"""
    serializer_class = ClubMembershipSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = ClubMembership.objects.all()
