from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsAdmin, IsSuperAdmin
from clubs.models import ClubEvent
from clubs.serializers import ClubEventSerializer


class AdminClubEventListCreateView(generics.ListCreateAPIView):
    """Admins can list all events or create a new event"""
    serializer_class = ClubEventSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = ClubEvent.objects.all().order_by('-event_date')

    def perform_create(self, serializer):
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
