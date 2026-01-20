from django.urls import path, include
from .views.auth.login import LoginView
from .views.auth.password_reset import PasswordResetRequestView, PasswordResetConfirmView
from .views.auth.verification import VerifyStudentAccountView, ResendVerificationOTPView
from .views.users.students import StudentRegisterView, StudentListView, StudentDetailView
from .views.users.admins import AdminListView, AdminDetailView
from .views.users.superadmin import SuperAdminUserView
from .views.users.profile import UserProfileView




urlpatterns = [
    path('register/', StudentRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/', SuperAdminUserView.as_view(), name='superadmin-users'),
    path('verify/', VerifyStudentAccountView.as_view(), name='verify-student'),
    path("resend/", ResendVerificationOTPView.as_view(), name="resend-verification-otp"),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('admins/', AdminListView.as_view(), name='admin-list'),
    path('admins/<int:pk>/', AdminDetailView.as_view(), name='admin-detail'),
]
