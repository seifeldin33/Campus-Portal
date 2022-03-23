from django.contrib import admin

# Register your models here.
from .models import Course, Doctor, \
    Student, User

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Doctor)
admin.site.register(Course)
