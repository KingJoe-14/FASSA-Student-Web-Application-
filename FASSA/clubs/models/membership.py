from django.db import models
from django.conf import settings
from .club import Club

User = settings.AUTH_USER_MODEL

class ClubMembership(models.Model):
    ROLE_CHOICES = [
        ('MEMBER', 'Member'),
        ('PRESIDENT', 'President'),
        ('VICE_PRESIDENT', 'Vice President'),
        ('SECRETARY', 'Secretary'),
        ('TREASURER', 'Treasurer'),
    ]

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'})
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEMBER')
    executive_photo = models.ImageField(upload_to='club_executives/', null=True, blank=True)
    executive_title = models.CharField(max_length=100, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('club', 'student')

    def __str__(self):
        return f"{self.student} - {self.club} ({self.role})"
