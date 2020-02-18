from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models


@login_required
def dashboard(request):

    return render(request, 'student/dashboard.html')


@login_required
def my_courses(request):

    return render(request, "student/my_courses.html", locals())









