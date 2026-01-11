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
    # Clubs
    path('clubs/', AdminClubListCreateView.as_view()),
    path('clubs/<int:pk>/', AdminClubRetrieveUpdateDeleteView.as_view()),

    # Members
    path('clubs/<int:club_id>/members/', AdminClubMemberListCreateView.as_view()),
    path('clubs/members/<int:pk>/', AdminClubMemberRetrieveUpdateDeleteView.as_view()),

    # Events
    path('events/', AdminClubEventListCreateView.as_view()),
    path('events/<int:pk>/', AdminClubEventRetrieveUpdateDeleteView.as_view()),


]
