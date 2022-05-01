from django.urls import path

from . import views

# if the link =  campus_portal/user/nour  user: url endpoint, nour: URL parameter
urlpatterns = [
    path('', views.get, name='home'),
    path('', views.index, name='index'),
    path('Login', views.login, name='Login'),
    path('Logout', views.logout, name='Logout'),
    path('student_signup', views.student_signup, name='student_signup'),
    path('doctor_signup', views.doctor_signup, name='doctor_signup'),
    path('create_course', views.create_course, name='create_course'),
    path('view_courses', views.view_courses, name='view_courses'),
    path('user/<str:user_name>', views.view_user_info, name='user_info'),
    path('user/<str:user_name>/edit', views.edit_user_info, name='edit_user_info'),
]
