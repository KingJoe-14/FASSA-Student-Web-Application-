# students/urls.py
from django.urls import path
from .views import (
    AvailableCoursesView,
    RegisterCourseView,
    MyCoursesView,
    PersonalTimetableView,
    AnnouncementListView,
    AnnouncementDetailViewForStudent
)

urlpatterns = [
    path('courses/', AvailableCoursesView.as_view(), name='available-courses'),
    path('register-course/', RegisterCourseView.as_view(), name='register-course'),
    path('my-courses/', MyCoursesView.as_view(), name='my-courses'),
    path('timetable/', PersonalTimetableView.as_view(), name='personal-timetable'),
    path('announcements/', AnnouncementListView.as_view(), name='announcement-list'),
    path('announcements/<int:pk>/', AnnouncementDetailViewForStudent.as_view(), name='announcement-detail'),

]
