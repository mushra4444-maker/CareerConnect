
from django.db import models
from django.contrib.auth.models import User
from jobportal.models import Job


class Application(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['job', 'candidate'],
                name='unique_candidate_job_application'
            )
        ]

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"


class Interview(models.Model):

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='interviews'
    )

    scheduled_at = models.DateTimeField()

    location_or_link = models.CharField(max_length=300)

    instructions = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_at']

    def __str__(self):
        return f"Interview - {self.application.candidate.username}"
