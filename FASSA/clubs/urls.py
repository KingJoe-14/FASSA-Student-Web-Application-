from django.urls import path
from clubs.views import (
    AdminClubListCreateView,
    AdminClubRetrieveUpdateDeleteView,
    AdminClubMemberListCreateView,
    AdminClubMemberRetrieveUpdateDeleteView,
    AdminClubEventListCreateView,
    AdminClubEventRetrieveUpdateDeleteView,
    AdminApproveClubEventView,   # ✅ MUST be imported
)
from clubs.views import ClubPresidentEventCreateView


urlpatterns = [
    # Clubs
    path('clubs/', AdminClubListCreateView.as_view()),
    path('clubs/<int:pk>/', AdminClubRetrieveUpdateDeleteView.as_view()),

    # Members
    path('clubs/<int:club_id>/members/', AdminClubMemberListCreateView.as_view()),
    path('clubs/members/<int:pk>/', AdminClubMemberRetrieveUpdateDeleteView.as_view()),

    # Events
    path('events/', AdminClubEventListCreateView.as_view()),
    path('events/<int:pk>/', AdminClubEventRetrieveUpdateDeleteView.as_view()),

    # ✅ EVENT APPROVAL
    path(
        'events/<int:pk>/approve/',
        AdminApproveClubEventView.as_view(),
        name='admin-approve-event'
    ),

    path(
        'clubs/<int:club_id>/president/events/',
        ClubPresidentEventCreateView.as_view(),
        name='club-president-event-create'
    ),
]
