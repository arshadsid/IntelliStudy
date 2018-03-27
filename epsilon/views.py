from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import (Course, Enroll, Student, Mentor, Question, ExtraInfo, Content, Manage)


def auth(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    print(username)
    user = authenticate(username = username, password = password)
    if user is not None:
        login(request, user)
        return redirect('/epsilon/dashboard')
    else:
        return redirect('/epsilon')


def index(request):
    context = {}
    return render(request, "epsilon/index.html", context)


def student(request):
    context = {}
    return render(request, "epsilon/loginstudent.html", context)


def mentor(request):
    context = {}
    return render(request, "epsilon/mentorlogin.html", context)


@login_required
def dashboard(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, "epsilon/student_dashboard.html", context)


@login_required
def course(request):
    cid = request.POST.get('course')
    course = Course.objects.get(Q(pk=cid))
    content = Content.objects.filter(Q(course_id=course))
    mentor = Mentor.objects.filter(Q(pk__in=Manage.objects.filter(Q(course_id=course)).values('mentor_id_id')))
    context = {'course': course, 'content': content, 'mentor': mentor}
    return render(request, "epsilon/coursemain.html", context)


@login_required
def quiz(request):
    context = {}
    return render(request, "epsilon/quiz.html", context)


@login_required
def mycourses(request):
    user = request.user
    course = Course.objects.filter(Q(pk__in=Enroll.objects.filter(Q(unique_id__in=Student.objects.filter(Q(unique_id__in=ExtraInfo.objects.filter(Q(user=user)))))).values('course_id_id')))
    context = {'courses': course}
    return render(request, "epsilon/mycourses.html", context)


@login_required
def profile(request):
    context = {}
    return render(request, "epsilon/profile.html", context)


@login_required
def study(request):
    context = {}
    return render(request, "epsilon/coursestudy.html", context)


@login_required
def group(request):
    context = {}
    return render(request, "epsilon/coursegroup.html", context)


def about(request):
    return render(request, 'epsilon/about.html')


@login_required
def loggedout(request):
    logout(request)
    return redirect('/epsilon')
