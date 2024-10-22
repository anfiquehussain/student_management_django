from django.db import models
from students.models import Student
from datetime import date

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class LibraryRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_on = models.DateField()
    returned_on = models.DateField(null=True, blank=True)
    return_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.student}"

    class Meta:
        verbose_name = "Library Record"
        verbose_name_plural = "Library Records"

    def save(self, *args, **kwargs):
        if self.return_status:
            self.returned_on = date.today()
        else:
            self.returned_on = None 
        
        super().save(*args, **kwargs)
