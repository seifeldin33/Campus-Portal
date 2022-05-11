from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.views.decorators.http import require_http_methods
from campus_portal.models import User, Student, Doctor, Course, StudentRegisterCourse
from django.utils.translation import gettext_lazy as _
import datetime
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError


# Create your views here.


def anonymous_required(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def index(request):
    context = {'title': 'SCS - Home'}
    return render(request, 'index.html', context)


@require_http_methods(["GET", "POST"])
@anonymous_required
def login(request):
    context = {'title': 'SCS - Login'}
    if request.method == "POST":
        u = auth.authenticate(username=request.POST['email'], password=request.POST['password'])
        if u is not None:
            auth.login(request, u)
            return redirect('home')
        else:
            try:
                username = User.objects.get(email=request.POST['email']).username
            except User.DoesNotExist:
                username = None
            u = auth.authenticate(username=username, password=request.POST['password'])
            if u is not None:
                auth.login(request, u)
                return redirect('home')
            context['error'] = "Username/Email or password is incorrect!"
    return render(request, 'User/Login.html', context)


def create_new_user(request, is_student=False, is_doctor=False):
    try:
        date = datetime.datetime.strptime(request.POST['birthdate'], "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        date = datetime.datetime.strptime(request.POST['birthdate'], "%d-%b-%Y").strftime("%Y-%m-%d")
    new_user = User(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                    gender=request.POST['gender'], username=request.POST['username'], email=request.POST['email'],
                    password=make_password(request.POST['password']), phone_number=request.POST['phone_number'],
                    birthdate=date, is_student=is_student, is_doctor=is_doctor)
    new_user.save()
    return new_user


# to use this decorator
@require_http_methods(["GET", "POST"])
@anonymous_required
def student_signup(request):
    context = {'title': 'SCS - Signup'}
    if request.method == "POST":
        if request.POST['password'] == request.POST['retyped_password']:
            if request.POST.get('terms', False) == 'agree':
                try:
                    User.objects.get(username=request.POST['username'])
                    context['error'] = 'Username is already taken!'
                except User.DoesNotExist:
                    try:
                        User.objects.get(username=request.POST['email'])
                        context['error'] = 'Email is already taken!'
                    except User.DoesNotExist:
                        new_user = create_new_user(request, is_student=True, is_doctor=False)
                        new_student = Student(user=new_user, school=request.POST['school'], major=request.POST['major'],
                                              concentration=request.POST['concentration'], level=1,
                                              cohort=datetime.date.today().year, gpa=0.0, percent=0.0,
                                              total_credit_hours=0, number_of_subjects=0)
                        new_student.save()
                        return redirect('Login')
            else:
                context['error'] = 'You must agree to the terms'
                return render(request, 'Student/signup.html', context)
        else:
            context['error'] = 'Password does not match!'

    return render(request, 'Student/signup.html', context)


@require_http_methods(["GET", "POST"])
@anonymous_required
def doctor_signup(request):
    context = {'title': 'SCS - Doctor Signup'}
    if request.method == "POST":
        if request.POST['password'] == request.POST['retyped_password']:
            if request.POST.get('terms', False) == 'agree':
                try:
                    User.objects.get(username=request.POST['username'])
                    context['error'] = 'Username is already taken!'
                except User.DoesNotExist:
                    try:
                        User.objects.get(username=request.POST['email'])
                        context['error'] = 'Email is already taken!'
                    except User.DoesNotExist:
                        new_user = create_new_user(request, is_student=False, is_doctor=True)
                        new_doctor = Doctor(user=new_user, degree=request.POST['degree'])
                        new_doctor.save()
                        return redirect('Login')
            else:
                context['error'] = 'You must agree to the terms'
                return render(request, 'Doctor/signup.html', context)
        else:
            context['error'] = 'Password does not match!'
        # new_user.
    return render(request, 'Doctor/signup.html', context)


@login_required
def view_user_info(request, user_name):
    context = {'title': 'SCS - information'}
    if user_name == request.user.username:
        if request.user.is_student:
            student = Student.objects.get(user=request.user.id)
            context["student"] = {'school': student.school, 'major': student.major,
                                  'concentration': student.concentration, 'level': student.level,
                                  'cohort': student.cohort, 'gpa': student.gpa, 'percent': student.percent,
                                  'total_credit_hours': student.total_credit_hours,
                                  'number_of_subjects': student.number_of_subjects,
                                  }
        if request.user.is_doctor:
            doctor = Doctor.objects.get(user=request.user.id)
            context["doctor"] = {'degree': doctor.degree}
        return render(request, 'User/view_info.html', context)
    else:
        context['error'] = "You Can't Show another user info"
        return render(request, 'index.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required
def create_course(request):
    context = {'title': 'SCS - Create Course'}
    if request.user.is_doctor:
        if request.method == "POST":
            new_course = Course(code=request.POST['code'], name=request.POST['name'],
                                credit_hour=request.POST['credit_hour'], prerequisite=request.POST['prerequisite'],
                                type=request.POST['type'])
            new_course.save()
            context["success"] = F"Course {new_course.name} Created Successfully"
        return render(request, 'Course/create_course.html', context)
    else:
        return redirect('home')


def view_courses(request):
    context = {'title': 'SCS - Courses'}
    all_courses = Course.objects.all().order_by('name')
    context["courses"] = all_courses
    return render(request, 'Course/view_courses.html', context)


@login_required
def edit_user_info(request, user_name):
    context = {'title': 'SCS - Edit User Info'}
    if request.method == "GET":
        if user_name == request.user.username:
            if request.user.is_student:
                student = Student.objects.get(user=request.user.id)
                context["student"] = {'school': student.school, 'major': student.major,
                                      'concentration': student.concentration,
                                      }
            if request.user.is_doctor:
                doctor = Doctor.objects.get(user=request.user.id)
                context["doctor"] = {'degree': doctor.degree}
    elif request.method == "POST":
        if user_name == request.user.username:
            user = User.objects.get(id=request.user.id)

            if request.POST.get("picture", True):
                user.picture = request.FILES['picture']

            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.gender = request.POST["gender"]

            # check if new username exist
            if request.POST["username"] != user.get_username():
                try:
                    User.objects.get(username=request.POST['username'])
                    context['error'] = 'Username is already taken!'
                    return render(request, 'User/edit_info.html', context)
                except User.DoesNotExist:
                    user.username = request.POST["username"]

            # check if new email exist
            if request.POST["email"] != user.email:
                try:
                    User.objects.get(email=request.POST['email'])
                    context['error'] = 'Email is already taken!'
                    return render(request, 'User/edit_info.html', context)
                except User.DoesNotExist:
                    user.email = request.POST["email"]

            if request.POST["password"] != "" and request.POST["password"] == request.POST["retyped_password"]:
                user.password = make_password(request.POST['password'])
            user.phone_number = request.POST["phone_number"]

            if request.POST["birthdate"] != "":
                try:
                    date = datetime.datetime.strptime(request.POST['birthdate'], "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    date = datetime.datetime.strptime(request.POST['birthdate'], "%d-%b-%Y").strftime("%Y-%m-%d")
                user.birthdate = date

            user.save()  # save changes after updates
            if user.is_student:
                student = Student.objects.get(user=user.id)
                student.school = request.POST["school"]
                student.major = request.POST["major"]
                student.concentration = request.POST["concentration"]
                student.save()  # save changes after updates

            if user.is_doctor:
                doctor = Doctor.objects.get(user=user.id)
                doctor.degree = request.POST["degree"]
                doctor.save()  # save changes after updates

            context["success"] = "your Info has been updated successfully"

    return render(request, 'User/edit_info.html', context)


@login_required
def be_student(request, user_name):
    if user_name == request.user.username:
        user = User.objects.get(id=request.user.id)
        user.is_student = True
        user.save()
        new_student = Student(user=user, school='', major='',
                              concentration='', level=1,
                              cohort=datetime.date.today().year, gpa=0.0, percent=0.0,
                              total_credit_hours=0, number_of_subjects=0)
        new_student.save()
        return redirect('user_info', user.get_username())
    return redirect('home')


@login_required
def be_doctor(request, user_name):
    if user_name == request.user.username:
        user = User.objects.get(id=request.user.id)
        user.is_doctor = True
        user.save()
        new_doctor = Doctor(user=user, degree='')
        new_doctor.save()
        return redirect('user_info', user.get_username())
    return redirect('home')


@login_required
def be_admin(request, user_name):
    if user_name == request.user.username:
        user = User.objects.get(id=request.user.id)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return redirect('user_info', user.get_username())
    return redirect('home')


@login_required
def visualization(request):
    context = {'title': 'SCS - Visualization'}
    if request.user.is_superuser:
        return render(request, 'visualization.html', context)
    return redirect('home')


@login_required
def view_course_info(request, course_id):
    context = {'title': 'SCS - Course info'}
    if request.user.is_student:
        student = Student.objects.get(user=request.user.id)
        try:
            course = Course.objects.get(id=course_id)
            context['course'] = course
            try:
                date_enrolled = StudentRegisterCourse.objects.get(course=course, student=student).date_enrolled
                context['enrolled'] = True
                context['date_enrolled'] = date_enrolled.date()
            except StudentRegisterCourse.DoesNotExist:
                context['enrolled'] = False
        except Course.DoesNotExist:
            context['error'] = "This Course doesn't Exist"
    else:
        context['error'] = "You Should be Student First to enroll in Course"
    return render(request, 'Course/view_info.html', context)


@login_required
def enroll_in_course(request, course_id):
    if request.user.is_student:
        course = Course.objects.get(id=course_id)
        student = Student.objects.get(user=request.user.id)
        try:
            StudentRegisterCourse.objects.get(course=course, student=student)
        except StudentRegisterCourse.DoesNotExist:
            StudentRegisterCourse(course=course, student=student).save()
    return redirect('course_info', course_id)
