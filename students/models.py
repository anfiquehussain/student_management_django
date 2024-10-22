from django.db import models
from django.core.exceptions import ValidationError
import re

class Class(models.Model):
    class_name = models.CharField(max_length=3, unique=True)

    def save(self, *args, **kwargs):
        self.class_name = self.class_name.upper()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.class_name


class Student(models.Model):
    full_name = models.CharField(max_length=50)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="students") 
    age = models.PositiveIntegerField()
    gender = models.CharField(
        max_length=1,
        choices=[
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Others')
        ]
    )
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    

    def __str__(self):
        return f"{self.full_name} ({self.class_name})"


class FeesRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fees_records")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_status = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Fees Record for {self.student} - Paid: {'Yes' if self.paid_status else 'No'}"
