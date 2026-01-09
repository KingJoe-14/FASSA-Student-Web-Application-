from rest_framework.permissions import BasePermission, SAFE_METHODS
from clubs.models import ClubMembership


class IsClubPresident(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        club_id = view.kwargs.get('club_id')
        if not club_id:
            return False
        return ClubMembership.objects.filter(
            student=request.user,
            club_id=club_id,
            role='PRESIDENT'
        ).exists()