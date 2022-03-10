from django.contrib import admin

# Register your models here.
from .models import Student, Doctor, Course

admin.site.register(Student)
admin.site.register(Doctor)
admin.site.register(Course)
