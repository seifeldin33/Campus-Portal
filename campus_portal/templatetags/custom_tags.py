from django import template
from ..models import Course, Student, Doctor, User, StudentRegisterCourse
from django.db.models import Count
from django.urls import reverse
import seaborn as sns

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


@register.simple_tag
def generate_color(palette=None, colors_number=None, alpha=1, desaturate=None):
    palette = None if palette == "" else palette
    colors = sns.color_palette(palette=palette, n_colors=colors_number, desat=desaturate)
    colors = [(round(r * 255, 2), round(g * 255, 2), round(b * 255, 2), round(alpha, 2)) for (r, g, b) in colors]
    return colors
