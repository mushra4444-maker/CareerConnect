from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):

    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    company = models.CharField(max_length=150)

    location = models.CharField(max_length=150)

    description = models.TextField()

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title