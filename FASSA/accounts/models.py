from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
import uuid
from django.utils import timezone
from datetime import timedelta
import random


class UserManager(BaseUserManager):
    """
    Custom manager for User model.
    Handles creation of students, admins, and superadmins.
    """

    def create_user(self, email, full_name, role='STUDENT', password=None, **extra_fields):
        """
        Creates and saves a regular user (student or admin).
        """
        if not email:
            raise ValueError("Users must have an email address.")
        if not full_name:
            raise ValueError("Users must have a full name.")

        email = self.normalize_email(email)


        user = self.model(email=email, full_name=full_name, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        """
        Creates and saves a superuser with all permissions.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'SUPERADMIN')

        return self.create_user(email=email, full_name=full_name, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model using email as username.
    Supports roles: SUPERADMIN, ADMIN, STUDENT.
    """
    ROLE_CHOICES = (
        ('SUPERADMIN', 'Super Admin'),
        ('ADMIN', 'Admin'),
        ('STUDENT', 'Student'),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    index_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.full_name} ({self.role})"

    def clean(self):
        pass


class AccountVerificationOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    def __str__(self):
        return f"{self.email} - {self.otp}"


class PasswordResetOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.email} - {self.otp}"

    @classmethod
    def generate_otp(cls):
        from random import randint
        return f"{randint(100000, 999999)}"
