from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.views.decorators.http import require_POST, require_http_methods
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
    print(request.path)
    return render(request, 'index.html', context)


def Login(request):
    context = {'title': 'N'}
    return render(request, 'Login.html', context)


def create_new_user(request):
    new_user = User(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                    username=request.POST['username'], email=request.POST['email'],
                    password=make_password(request.POST['password']), phone_number=request.POST['phone_number'],
                    birthdate=datetime.datetime.strptime(request.POST['birthdate'], "%d-%b-%Y").
                    strftime("%Y-%m-%d"))
    new_user.save()
    return new_user


# to use this decorator
@require_http_methods(["GET", "POST"])
@anonymous_required
def student_signup(request):
    context = {'title': 'Signup'}
    if request.method == "POST":
        print(request.POST)
        if request.POST['password'] == request.POST['retyped_password']:
            if request.POST['terms'] == 'agree':
                try:
                    User.objects.get(username=request.POST['username'])
                    context['error'] = 'Username is already taken!'
                except User.DoesNotExist:
                    new_user = create_new_user(request)
                    new_student = Student(user=new_user, school=request.POST['school'], major=request.POST['major'],
                                          concentration=request.POST['concentration'], level=1,
                                          cohort=datetime.date.today().year, gpa=0.0, percent=0.0, total_credit_hours=0,
                                          number_of_subjects=0)
                    new_student.save()
                    return redirect('Login')
            else:
                return render(request, 'Student/signup.html', context)
        else:
            context['error'] = 'Password does not match!'

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
                    context['error'] = 'Username is already taken!'
                except User.DoesNotExist:
                    new_user = create_new_user(request)
                    new_doctor = Doctor(user=new_user, degree=request.POST['degree'])
                    new_doctor.save()
                    return redirect('Login')
            else:
                return render(request, 'Doctor/signup.html', context)
        else:
            context['error'] = 'Password does not match!'
        print(request.POST)
        print(request.POST['first_name'])
        # new_user.
    return render(request, 'Doctor/signup.html', context)


#
# def signup(request):
#     if request.method == "POST":
#         pass
#     if request.POST['password1'] == request.POST['password2']:
#         try:
#             User.objects.get(username=request.POST['username'])
#             return render(request, 'accounts/signup.html', {'error': 'Username is already taken!'})
#         except User.DoesNotExist:
#             user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
#             auth.login(request, user)
#             return redirect('home')
#     else:
#         return render(request, 'accounts/signup.html', {'error': 'Password does not match!'})
# else:
#     return render(request, 'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        pass
    #     user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
    #     if user is not None:
    #         auth.login(request, user)
    #         return redirect('home')
    #     else:
    #         return render(request, 'accounts/login.html', {'error': 'Username or password is incorrect!'})
    # else:
    #     return render(request, 'accounts/login.html')


@login_required
def logout(request):
    pass
    # if request.method == 'POST':
    #     auth.logout(request)
    # return redirect('home')
