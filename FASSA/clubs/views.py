from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from accounts.permissions import IsAdmin, IsSuperAdmin
from clubs.models import Club, ClubMembership, ClubEvent
from clubs.serializers import ClubSerializer, ClubMembershipSerializer, ClubEventSerializer
from accounts.models import User


# -------------------------------
# CLUB CRUD (Admins & Superadmins)
# -------------------------------
class AdminClubListCreateView(generics.ListCreateAPIView):
    """
    List all clubs or create a new club (Admin/Superadmin)
    """
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = Club.objects.all().order_by('-created_at')


class AdminClubRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a club
    """
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = Club.objects.all()


# -------------------------------
# CLUB MEMBERSHIPS (Assign Leaders/Executives)
# -------------------------------
class AdminClubMemberListCreateView(generics.ListCreateAPIView):
    """
    List members of a club or add a student to a club (with role)
    """
    serializer_class = ClubMembershipSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]

    def get_queryset(self):
        club_id = self.kwargs.get('club_id')
        return ClubMembership.objects.filter(club_id=club_id)

    def perform_create(self, serializer):
        club_id = self.kwargs.get('club_id')
        serializer.save(club_id=club_id)


class AdminClubMemberRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update (role), or remove a member from a club
    """
    serializer_class = ClubMembershipSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = ClubMembership.objects.all()


# -------------------------------
# CLUB EVENTS (Approve/Manage)
# -------------------------------
class AdminClubEventListCreateView(generics.ListCreateAPIView):
    """
    List events for all clubs or create a new event
    """
    serializer_class = ClubEventSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = ClubEvent.objects.all().order_by('-event_date')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AdminClubEventRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update (approve/reject), or delete a club event
    """
    serializer_class = ClubEventSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = ClubEvent.objects.all()
