from django.db import models


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField()
    MALE, FEMALE = 'M', 'F'
    TEMP_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )
    gender = models.CharField(max_length=1, choices=TEMP_CHOICES, default=MALE)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    national_id = models.IntegerField(max_length=14)
    name_in_arabic = models.CharField(max_length=100)
    address_in_arabic = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    citizenship = models.CharField(max_length=20)
    mother_tongue = models.CharField(max_length=20)
    birth_place = models.CharField(max_length=100)
    zip_code = models.CharField(null=True, max_length=5)
    picture = models.ImageField(null=True)
    admitted_in = models.DateField(auto_created=True)

    class Meta:
        abstract = True


class Student(Person):
    Student_ID = models.IntegerField(primary_key=True, unique=True)
    program = models.CharField(max_length=10)
    school = models.CharField(max_length=10)
    major = models.CharField(max_length=10)
    concentration = models.CharField(max_length=10)
    level = models.IntegerField(default=1)
    cohort = models.IntegerField()
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    percent = models.DecimalField(max_digits=4, decimal_places=2)
    admission_status = models.CharField(max_length=10)
    academic_status = models.CharField(max_length=10)
    total_credit_hours = models.IntegerField()
    number_of_subjects = models.IntegerField()
    thanawya_grade = models.DecimalField(max_digits=4, decimal_places=2)
    thanawya_percent = models.DecimalField(max_digits=4, decimal_places=2)
    thanawya_type = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Employee(Person):
    employee_ID = models.IntegerField(primary_key=True, unique=True)
    department = models.CharField(max_length=10)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Doctor(Employee):
    degree = models.CharField(max_length=10)


class Course(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=40)
    credit_hour = models.IntegerField()
    prerequistes = models.CharField(null=True, max_length=10)
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.name
