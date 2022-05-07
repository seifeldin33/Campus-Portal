from django.contrib import admin

# Register your models here.
from .models import Course, Doctor, \
    Student, User, StudentRegisterCourse

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Doctor)
admin.site.register(Course)
admin.site.register(StudentRegisterCourse)
