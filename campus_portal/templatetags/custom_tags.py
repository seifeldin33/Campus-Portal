from django import template
from ..models import Course, Student, Doctor
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
