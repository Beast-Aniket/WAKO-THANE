from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('ACADEMY', 'Academy'),
        ('PLAYER', 'Player'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PLAYER')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
