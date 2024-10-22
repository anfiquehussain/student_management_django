# library/admin.py
from django.contrib import admin
from .models import LibraryRecord,Book

admin.site.register(LibraryRecord)
admin.site.register(Book)

