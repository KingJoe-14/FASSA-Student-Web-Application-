from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from accounts.permissions import IsAdmin, IsSuperAdmin
from clubs.models import Club, ClubMembership, ClubEvent
from clubs.serializers import (
    ClubSerializer,
    ClubMembershipSerializer,
    ClubEventSerializer,
)


# -------------------------------
# CLUB CRUD (Admins & Superadmins)
# -------------------------------
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


# -------------------------------
# CLUB MEMBERSHIPS (Assign Leaders/Executives)
# -------------------------------
class AdminClubMemberListCreateView(generics.ListCreateAPIView):
    """List members of a club or add a new member (Admin/Superadmin)"""
    serializer_class = ClubMembershipSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]

    def get_queryset(self):
        club_id = self.kwargs['club_id']
        return ClubMembership.objects.filter(club_id=club_id)

    def get_serializer_context(self):
        """Pass the club instance to the serializer"""
        context = super().get_serializer_context()
        context['club'] = get_object_or_404(Club, id=self.kwargs['club_id'])
        return context


class AdminClubMemberRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update (role), or remove a member from a club"""
    serializer_class = ClubMembershipSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = ClubMembership.objects.all()


# -------------------------------
# CLUB EVENTS (Admins create/manage)
# -------------------------------
class AdminClubEventListCreateView(generics.ListCreateAPIView):
    """Admins can list all events or create a new event"""
    serializer_class = ClubEventSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = ClubEvent.objects.all().order_by('-event_date')

    def perform_create(self, serializer):
        """Automatically assign the admin who created the event"""
        serializer.save(created_by=self.request.user)


class AdminClubEventRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Admins can retrieve, update, or delete events"""
    serializer_class = ClubEventSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = ClubEvent.objects.all()

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        self.perform_destroy(event)
        return Response(
            {"message": f"Event '{event.title}' deleted successfully."},
            status=status.HTTP_200_OK
        )
