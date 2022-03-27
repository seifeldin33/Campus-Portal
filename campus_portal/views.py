from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.views.decorators.http import require_http_methods
from campus_portal.models import User, Student, Doctor
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
    return HttpResponse(F"Hello, world. You're {request.user}")


def get(request):
    context = {'title': 'N'}
    return render(request, 'index.html', context)


@require_http_methods(["GET", "POST"])
@anonymous_required
def login(request):
    context = {'title': 'Login'}
    if request.method == "POST":
        u = auth.authenticate(username=request.POST['email'], password=request.POST['password'])
        if u is not None:
            auth.login(request, u)
            return redirect('home')
        else:
            u = auth.authenticate(email=request.POST['email'], password=request.POST['password'])
            if u is not None:
                auth.login(request, u)
                return redirect('home')
            context['errors'] = "'Username/Email or password is incorrect!"
    return render(request, 'Login.html', context)


def create_new_user(request, is_student=False, is_doctor=False):
    try:
        date = datetime.datetime.strptime(request.POST['birthdate'], "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        date = datetime.datetime.strptime(request.POST['birthdate'], "%d-%b-%Y").strftime("%Y-%m-%d")
    new_user = User(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                    username=request.POST['username'], email=request.POST['email'],
                    password=make_password(request.POST['password']), phone_number=request.POST['phone_number'],
                    birthdate=date, is_student=is_student, is_doctor=is_doctor)
    new_user.save()
    return new_user


# to use this decorator
@require_http_methods(["GET", "POST"])
@anonymous_required
def student_signup(request):
    context = {'title': 'Signup'}
    if request.method == "POST":
        if request.POST['password'] == request.POST['retyped_password']:
            if request.POST['terms'] == 'agree':
                try:
                    User.objects.get(username=request.POST['username'])
                    context['errors'] = 'Username is already taken!'
                except User.DoesNotExist:
                    try:
                        User.objects.get(username=request.POST['email'])
                        context['errors'] = 'Email is already taken!'
                    except User.DoesNotExist:
                        new_user = create_new_user(request, is_student=True, is_doctor=False)
                        new_student = Student(user=new_user, school=request.POST['school'], major=request.POST['major'],
                                              concentration=request.POST['concentration'], level=1,
                                              cohort=datetime.date.today().year, gpa=0.0, percent=0.0,
                                              total_credit_hours=0, number_of_subjects=0)
                        new_student.save()
                        return redirect('Login')
            else:
                context['errors'] = 'You must agree to the terms'
                return render(request, 'Student/signup.html', context)
        else:
            context['errors'] = 'Password does not match!'

    return render(request, 'Student/signup.html', context)


@require_http_methods(["GET", "POST"])
@anonymous_required
def doctor_signup(request):
    context = {'title': 'Signup'}
    if request.method == "POST":
        if request.POST['password'] == request.POST['retyped_password']:
            if request.POST['terms'] == 'agree':
                try:
                    User.objects.get(username=request.POST['username'])
                    context['errors'] = 'Username is already taken!'
                except User.DoesNotExist:
                    try:
                        User.objects.get(username=request.POST['email'])
                        context['errors'] = 'Email is already taken!'
                    except User.DoesNotExist:
                        new_user = create_new_user(request, is_student=False, is_doctor=True)
                        new_doctor = Doctor(user=new_user, degree=request.POST['degree'])
                        new_doctor.save()
                        return redirect('Login')
            else:
                context['errors'] = 'You must agree to the terms'
                return render(request, 'Doctor/signup.html', context)
        else:
            context['errors'] = 'Password does not match!'
        # new_user.
    return render(request, 'Doctor/signup.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')
