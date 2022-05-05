from django import template
from ..models import Course, Student, Doctor, User, StudentRegisterCourse
from django.db.models import Count
from django.urls import reverse

register = template.Library()


@register.simple_tag
def active(current_link, active_link):
    if current_link == reverse(active_link):
        return "active"
    else:
        return ""


@register.simple_tag
def active_in(current_link, active_link):
    if active_link in current_link:
        return "active"
    else:
        return ""


@register.simple_tag
def courses_number():
    return Course.objects.count()


@register.simple_tag
def students_number():
    return Student.objects.count()


@register.simple_tag
def doctors_number():
    return Doctor.objects.count()


@register.simple_tag
def users_number():
    return User.objects.count()


@register.simple_tag
def number_user_per_gender():
    result = (User.objects.values('gender').annotate(count=Count('gender')).order_by())
    return result[::-1]


@register.simple_tag
def number_student_per_school():
    result = (Student.objects.values('school').annotate(count=Count('school')).order_by())
    return result[::-1]


@register.simple_tag
def number_student_per_course():
    result = (StudentRegisterCourse.objects.values('course').annotate(count=Count('course')).order_by())
    return result


@register.simple_tag
def name_course(course_id):
    try:
        name = Course.objects.get(id=course_id).name
    except Course.DoesNotExist:
        name = ""
    return name
