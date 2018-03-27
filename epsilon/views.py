from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
    user = request.user
    context = {}
    return render(request, "epsilon/student_dashboard.html", context)


@login_required
def course(request):
    context = {}
    return render(request, "epsilon/coursemain.html", context)


@login_required
def quiz(request):
    context = {}
    return render(request, "epsilon/quiz.html", context)


@login_required
def mycourses(request):
    context = {}
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
