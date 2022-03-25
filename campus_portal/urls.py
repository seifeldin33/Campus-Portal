from django.urls import path

from . import views

urlpatterns = [
    path('', views.get, name='home'),
    path('', views.index, name='index'),
    path('Login', views.login, name='Login'),
    path('Logout', views.logout, name='Logout'),
    path('student_signup', views.student_signup, name='student_signup'),
    path('doctor_signup', views.doctor_signup, name='doctor_signup'),
]
