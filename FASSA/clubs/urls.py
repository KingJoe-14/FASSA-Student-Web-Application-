from django.urls import path
from clubs.views import (
    AdminClubListCreateView,
    AdminClubRetrieveUpdateDeleteView,
    AdminClubMemberListCreateView,
    AdminClubMemberRetrieveUpdateDeleteView,
    AdminClubEventListCreateView,
    AdminClubEventRetrieveUpdateDeleteView,
)

urlpatterns = [
    # -------------------------------
    # CLUBS CRUD
    # -------------------------------
    path('clubs/', AdminClubListCreateView.as_view(), name='admin-club-list-create'),
    path('clubs/<int:pk>/', AdminClubRetrieveUpdateDeleteView.as_view(), name='admin-club-detail'),

    # -------------------------------
    # CLUB MEMBERSHIPS (leaders/executives)
    # -------------------------------
    path(
        'clubs/<int:club_id>/members/',
        AdminClubMemberListCreateView.as_view(),
        name='admin-club-member-list-create'
    ),
    path(
        'clubs/members/<int:pk>/',
        AdminClubMemberRetrieveUpdateDeleteView.as_view(),
        name='admin-club-member-detail'
    ),

    # -------------------------------
    # CLUB EVENTS
    # -------------------------------
    path('events/', AdminClubEventListCreateView.as_view(), name='admin-club-event-list-create'),
    path('events/<int:pk>/', AdminClubEventRetrieveUpdateDeleteView.as_view(), name='admin-club-event-detail'),
]
