from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField('student status', default=False)
    is_doctor = models.BooleanField('teacher status', default=False)
    birthdate = models.DateField(blank=True, null=True)
    MALE, FEMALE = 'M', 'F'
    TEMP_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))
    gender = models.CharField(max_length=1, choices=TEMP_CHOICES, default=MALE)
    phone_number = models.CharField(max_length=15, default="01000000000")
    picture = models.ImageField(null=True, upload_to="uploads/students_picture/")

    def __str__(self):
        # return self.username.strip()
        string_name = (self.first_name + " " + self.last_name).strip()
        if string_name == "":
            string_name = self.username.strip()
        return string_name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    school = models.CharField(max_length=10)
    major = models.CharField(max_length=10)
    concentration = models.CharField(max_length=10)
    level = models.IntegerField(default=1)
    cohort = models.IntegerField()

    def validate_gpa(gpa):
        if gpa > 4:
            raise ValidationError(r"No one's GPA is greater than 4")
        elif gpa < 0:
            raise ValidationError(r"No one's GPA is smaller than 0")

    gpa = models.DecimalField(max_digits=4, decimal_places=2, validators=[validate_gpa])
    percent = models.DecimalField(max_digits=4, decimal_places=2)
    total_credit_hours = models.IntegerField()
    number_of_subjects = models.IntegerField()

    def __str__(self):
        return (self.user.first_name + " " + self.user.last_name).strip()

    class Meta:
        ordering = ["user"]


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    degree = models.CharField(max_length=10)

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return ("Dr. " + self.user.first_name + " " + self.user.last_name).strip()


class Course(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=40)
    credit_hour = models.IntegerField()
    prerequisite = models.CharField(null=True, max_length=10)
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.name.strip()

    class Meta:
        ordering = ["-name"]
