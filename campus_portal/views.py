from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User


# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def get(request):
    context = {'title': 'N'}
    return render(request, 'index.html', context)


def Login(request):
    context = {'title': 'N'}
    return render(request, 'Login.html', context)


def signup(request):
    if request.method == "POST":
        print(request)
        print(request.read())
    context = {'title': 'N'}
    return render(request, 'signup.html', context)


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


def logout(request):
    pass
    # if request.method == 'POST':
    #     auth.logout(request)
    # return redirect('home')
