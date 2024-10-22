# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # You can add any additional fields if needed
    role = models.CharField(max_length=50, choices=[
        ('Admin', 'Admin'),
        ('Office Staff', 'Office Staff'),
        ('Librarian', 'Librarian')
    ])
    def save(self, *args, **kwargs):
        # Check if the role is 'Admin' and set is_superuser accordingly
        if self.is_superuser:
            self.role = 'Admin'
            
        super().save(*args, **kwargs)
