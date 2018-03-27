from django.shortcuts import render


def index(request):
    context = {}
    return render(request, "epsilon/index.html", context)


def student(request):
    context = {}
    return render(request, "epsilon/loginstudent.html", context)


def mentor(request):
    context = {}
    return render(request, "epsilon/mentorlogin.html", context)


def dashboard(request):
    context = {}
    return render(request, "epsilon/student_dashboard.html", context)


def course(request):
    context = {}
    return render(request, "epsilon/coursemain.html", context)


def quiz(request):
    context = {}
    return render(request, "epsilon/quiz.html", context)


def mycourses(request):
    context = {}
    return render(request, "epsilon/mycourses.html", context)


def profile(request):
    context = {}
    return render(request, "epsilon/profile.html", context)


def study(request):
    context = {}
    return render(request, "epsilon/coursestudy.html", context)


def group(request):
    context = {}
    return render(request, "epsilon/coursegroup.html", context)


def about(request):
    return render(request, 'epsilon/about.html')
