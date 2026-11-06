
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    full_name = models.CharField(
        max_length=150,
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    location = models.CharField(
        max_length=150,
        blank=True
    )

    skills = models.TextField(blank=True)

    education = models.CharField(
        max_length=200,
        blank=True
    )

    summary = models.TextField(blank=True)

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username
