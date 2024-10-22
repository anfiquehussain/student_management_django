# students/admin.py
from django.contrib import admin
from .models import Student,FeesRecord,Class

admin.site.register(Student)
admin.site.register(FeesRecord)
admin.site.register(Class)

