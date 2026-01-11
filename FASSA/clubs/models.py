from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Club(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='club_logos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ClubMembership(models.Model):

    ROLE_CHOICES = [
        ('MEMBER', 'Member'),
        ('PRESIDENT', 'President'),
        ('VICE_PRESIDENT', 'Vice President'),
        ('SECRETARY', 'Secretary'),
        ('TREASURER', 'Treasurer'),
    ]

    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name='memberships'
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'STUDENT'}
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='MEMBER'
    )

    # 🔹 Executive-only display fields
    executive_photo = models.ImageField(
        upload_to='club_executives/',
        null=True,
        blank=True
    )

    executive_title = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional title like 'Head of Operations'"
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('club', 'student')

    def __str__(self):
        return f"{self.student} - {self.club} ({self.role})"


class ClubEvent(models.Model):
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name='events'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.club.name})"

