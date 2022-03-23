# from django.db import models
# from django.core.exceptions import ValidationError
#
#
# # Create your models here.
# class Person(models.Model):
#     name = models.CharField(max_length=100)
#     birthdate = models.DateField()
#     MALE, FEMALE = 'M', 'F'
#     TEMP_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))
#     gender = models.CharField(max_length=1, choices=TEMP_CHOICES, default=MALE)
#     email = models.EmailField()
#     phone_number = models.CharField(max_length=15)
#     address = models.CharField(max_length=100)
#     national_id = models.IntegerField(max_length=14)
#     name_in_arabic = models.CharField(max_length=100)
#     address_in_arabic = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     citizenship = models.CharField(max_length=20)
#     mother_tongue = models.CharField(max_length=20)
#     birth_place = models.CharField(max_length=100)
#     zip_code = models.CharField(null=True, max_length=5)
#     picture = models.ImageField(null=True, upload_to="uploads/students_picture/")
#     admitted_in = models.DateField(auto_now_add=True)
#
#     class Meta:
#         abstract = True
#
#     def save(self, *args, **kwargs):
#         r = int(str(self.national_id)[-2]) % 2
#         if (r == 0) and (self.gender == "M"):
#             raise ValidationError('You Entered Fake National ID')
#         if (r == 1) and (self.gender == "F"):
#             raise ValidationError('You Entered Fake National ID')
#         self.full_clean()
#         super(Person, self).save(*args, **kwargs)
#
#
# class Student(Person):
#     Student_ID = models.IntegerField(primary_key=True, unique=True)
#     program = models.CharField(max_length=10)
#     school = models.CharField(max_length=10)
#     major = models.CharField(max_length=10)
#     concentration = models.CharField(max_length=10)
#     level = models.IntegerField(default=1)
#     cohort = models.IntegerField()
#
#     def validate_gpa(gpa):
#         if gpa > 4:
#             raise ValidationError(r"No one's GPA is greater than 4")
#         elif gpa < 0:
#             raise ValidationError(r"No one's GPA is smaller than 0")
#
#     gpa = models.DecimalField(max_digits=4, decimal_places=2, validators=[validate_gpa])
#     percent = models.DecimalField(max_digits=4, decimal_places=2)
#     admission_status = models.CharField(max_length=10)
#     academic_status = models.CharField(max_length=10)
#     total_credit_hours = models.IntegerField()
#     number_of_subjects = models.IntegerField()
#     thanawya_grade = models.DecimalField(max_digits=4, decimal_places=2)
#     thanawya_percent = models.DecimalField(max_digits=4, decimal_places=2)
#     thanawya_type = models.CharField(max_length=10)
#
#     def __str__(self):
#         return self.name
#
#
# class Meta:
#     ordering = ["-Student_ID", "name"]
#
#
# class Employee(Person):
#     employee_ID = models.IntegerField(primary_key=True, unique=True)
#     department = models.CharField(max_length=10)
#     salary = models.FloatField()
#
#     def __str__(self):
#         return self.name
#
#
# class Doctor(Employee):
#     degree = models.CharField(max_length=10)
#
#     class Meta:
#         ordering = ["name"]
#
#
# class Course(models.Model):
#     code = models.CharField(primary_key=True, max_length=10)
#     name = models.CharField(max_length=40)
#     credit_hour = models.IntegerField()
#     pre_requistes = models.CharField(null=True, max_length=10)
#     type = models.CharField(max_length=10)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ["-name"]

"""
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField()
    MALE, FEMALE = 'M', 'F'
    TEMP_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))
    gender = models.CharField(max_length=1, choices=TEMP_CHOICES, default=MALE)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    picture = models.ImageField(null=True, upload_to="uploads/students_picture/")
    admitted_in = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Person, self).save(*args, **kwargs)


class Student(Person):
    Student_ID = models.IntegerField(primary_key=True, unique=True)
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
        return self.name

    class Meta:
        ordering = ["-Student_ID", "name"]


class Employee(Person):
    employee_ID = models.IntegerField(primary_key=True, unique=True)
    department = models.CharField(max_length=10)
    salary = models.FloatField()

    def __str__(self):
        return self.name


class Doctor(Employee):
    degree = models.CharField(max_length=10)

    class Meta:
        ordering = ["name"]


class Course(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=40)
    credit_hour = models.IntegerField()
    pre_requistes = models.CharField(null=True, max_length=10)
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-name"]
"""
