import random


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from .models import (Course, Enroll, Student, Mentor, Question, ExtraInfo, Content, Manage, Score,
                     File, Option, Contain, Group, Career, Has)




def auth(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username = username, password = password)
    extrainfo = ExtraInfo.objects.get(user=user)
    if extrainfo.user_type == "student":
        student = Student.objects.get(unique_id=extrainfo)
        score = Score.objects.filter(unique_id=student)
        counter = 0
        flag = 0
        for s in score:
            if s.marks != -1:
                counter = counter + 10
                flag = flag + s.marks
        if counter > 0:
            avg = (flag * 100)/counter
            if avg > 80:
                student.level = "advanced"
            elif avg > 60:
                student.level = "intermediate"
            else:
                stduent.level = "beginner"
    if user is not None:
        login(request, user)
        if extrainfo.user_type == "student":
            return redirect('/epsilon/dashboard')
        else:
            return rediect('/epsilon/mdashboard')
    else:
        return redirect('/epsilon')

def signup(request):
    if 'student' in request.POST:
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(password)
        user, created = User.objects.get_or_create(username = username)
        if created:
            user.set_password(password)
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.save()
        gender = request.POST.get("gender")
        job = request.POST.get("job")
        qualification = request.POST.get("qualification")
        dob = request.POST.get("dob")
        info = ExtraInfo(user=user , sex=gender, date_of_birth=dob, user_type="student", job=job, qualification=qualification)
        info.save()
        stud = Student(unique_id=info, level="beginner")
        stud.save()
        login(request, user)
        return redirect('/epsilon/dashboard')
    else:
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(password)
        user, created = User.objects.get_or_create(username = username)
        if created:
            user.set_password(password)
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.save()
        gender = request.POST.get("gender")
        job = request.POST.get("job")
        qualification = request.POST.get("qualification")
        dob = request.POST.get("dob")
        info = ExtraInfo(user=user , sex=gender, date_of_birth=dob, user_type="mentor", job=job, qualification=qualification)
        info.save()
        mentor = Mentor(mentor_id=info)
        mentor.save()
        login(request, user)
        return redirect('/epsilon/mdashboard')

    # return HttpResponse("successfully signed up")

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
    career = Career.objects.all()
    context = {'courses': courses, 'career': career}
    return render(request, "epsilon/student_dashboard.html", context)


@login_required
def course(request):
    user = request.user
    if 'course' in request.POST:
        cid = request.POST.get('course')
        course = Course.objects.get(Q(pk=cid))
        enroll = Enroll.objects.filter(Q(unique_id=Student.objects.get(unique_id=ExtraInfo.objects.get(user=user)),
                                         course_id=course))
    if 'join' in request.POST:
        cid = request.POST.get('join')
        course = Course.objects.get(Q(pk=cid))
        enroll = Enroll.objects.create(course_id=course, unique_id=Student.objects.get(unique_id=ExtraInfo.objects.get(user=user)))
        content = Content.objects.filter(Q(course_id=course))
        for c in content:
            score = Score.objects.create(content_id = c, unique_id=Student.objects.get(unique_id=ExtraInfo.objects.get(user=user)))
        enroll.save()
    if 'leave' in request.POST:
        cid = request.POST.get('leave')
        course = Course.objects.get(Q(pk=cid))
        enroll = Enroll.objects.filter(Q(unique_id=Student.objects.get(unique_id=ExtraInfo.objects.get(user=user)),
                                         course_id=course))
        content = Content.objects.filter(Q(course_id=course))
        contain = Contain.objects.filter(Q(group_id=Group.objects.get(course_id=course),
                                           unique_id=Student.objects.get(unique_id=ExtraInfo.objects.get(user=user))))
        if contain.exists():
            contain.delete()
        for c in content:
            score = Score.objects.filter(Q(content_id = c, unique_id=Student.objects.get(unique_id=ExtraInfo.objects.get(user=user))))
            score.delete()
        enroll.delete()
    if 'feedback' in request.POST:
        cid = request.POST.get('feedback')
        course = Course.objects.get(Q(pk=cid))
        enroll = Enroll.objects.get(unique_id=Student.objects.get(unique_id=ExtraInfo.objects.get(user=user)),
                                         course_id=course)
        enroll.feedback = request.POST.get('text')
        enroll.save()
    content = Content.objects.filter(Q(course_id=course))
    score = Score.objects.filter(Q(unique_id=Student.objects.get(unique_id=ExtraInfo.objects.get(user=user)),
                                   content_id__in=content))
    flag=0
    counter=0
    for s in score:
        counter=counter+1
        if s.progress == "COMPLETED":
            flag=flag+1
    if counter != 0:
        progress = (flag * 100)/counter
    else:
        progress = 0
    mentor = Mentor.objects.filter(Q(pk__in=Manage.objects.filter(Q(course_id=course)).values('mentor_id_id')))
    group = Group.objects.filter(Q(course_id=course))
    if group:
        contain = Contain.objects.filter(Q(group_id=Group.objects.get(course_id=course),
                                           unique_id=Student.objects.get(unique_id=ExtraInfo.objects.get(user=user))))
    else:
        contain = []
    context = {'course': course, 'content': content, 'mentor': mentor, 'enroll': enroll, 'score': score, 'progress': progress, 'contain': contain}
    return render(request, "epsilon/coursemain.html", context)


@login_required
def career(request):
    user = request.user
    if 'career' in request.POST:
        career_id = request.POST.get('career')
        career = Career.objects.get(Q(pk=career_id))
        has = sorted(Has.objects.filter(Q(career_id=career)), key=lambda t: t.order)
        print(has)
    context = {'career': career, 'has': has}
    return render(request, "epsilon/careerpath.html", context)


@login_required
def quiz(request):
    if 'givequiz' in request.POST:
        cid = request.POST.get('givequiz')
        content = Content.objects.get(pk=cid)
        user=request.user
        unique_id=Student.objects.get(unique_id=ExtraInfo.objects.get(user=user))
        quiz = Question.objects.filter(Q(content_id=content, level=unique_id.level))
        questions = random.sample(list(quiz), 10)
        option = Option.objects.filter(Q(question_id__in=questions))
        context = {'content': content, 'questions': questions, 'option': option}
        return render(request, "epsilon/quiz.html", context)
    if 'give' in request.POST:
        questions1 = request.POST['give']
        print(type(questions1))
        #option = Option.objects.filter(Q(question_id__in=questions))
        content = Question.objects.filter(Q(pk__in=questions1)).values('content_id_id')
        for q in questions1:
            o = request.POST.get('q.question','')
            if o == q.answer:
                a['q'] = "correct"
            else:
                a['q'] = "incorrect"
        context = {'content': content, 'questions': questions1, 'option': option, 'a': a}
        return render(request, "epsilon/quiz.html", context)


@login_required
def mycourses(request):
    user = request.user
    course = Course.objects.filter(Q(pk__in=Enroll.objects.filter(Q(unique_id__in=Student.objects.filter(Q(unique_id__in=ExtraInfo.objects.filter(Q(user=user)))))).values('course_id_id')))
    context = {'courses': course}
    return render(request, "epsilon/mycourses.html", context)


@login_required
def profile(request):
    user = request.user
    extrainfo = ExtraInfo.objects.get(user=user)
    context = {'extrainfo': extrainfo, 'user':user}
    return render(request, "epsilon/profile.html", context)

@login_required
def update_profile(request):
    user = request.user
    extrainfo = ExtraInfo.objects.get(user=user)
    job = request.POST.get("job_opt")
    qualification = request.POST.get("qualify_opt")
    password = request.POST.get("password")
    extrainfo.job = job
    extrainfo.qualification = qualification
    extrainfo.save()
    user.set_password(password)
    user.save()
    context = {'extrainfo': extrainfo, 'user':user}

    profile(request)
    return render(request, "epsilon/profile.html", context)

@login_required
def study(request):
    cid = request.POST.get('content')
    content = Content.objects.get(pk=cid)
    file = File.objects.filter(Q(content_id=content))
    user=request.user
    unique_id=Student.objects.get(unique_id=ExtraInfo.objects.get(user=user))
    quiz = Question.objects.filter(Q(content_id=content, level=unique_id.level))
    context = {'content': content, 'file': file}
    return render(request, "epsilon/coursestudy.html", context)


@login_required
def group(request):
    user = request.user
    if 'group' in request.POST:
        cid = request.POST.get('group')
        course = Course.objects.get(pk=cid)
        contain = Contain.objects.get(group_id__in=Group.objects.filter(Q(course_id=course)),
                                      unique_id=Student.objects.get(unique_id=ExtraInfo.objects.get(user=user)))
        students = Student.objects.filter(Q(unique_id__in=Contain.objects.filter(Q(group_id=Group.objects.filter(Q(course_id=course)))).values('unique_id_id')))
        context = {'course': course, 'students': students}
        return render(request, "epsilon/coursegroup.html", context)
    if 'join' in request.POST:
        cid = request.POST.get('join')
        course = Course.objects.get(pk=cid)
        flag = 0
        student = Student.objects.get(unique_id=ExtraInfo.objects.get(user=user))
        group=Group.objects.filter(Q(course_id=course, level=student.level))
        for g in group:
            contain = Contain.objects.filter(Q(group_id=g))
            counter = 0
            for c in contain:
                counter = counter + 1
            if counter<5:
                contain = Contain.objects.create(group_id=g, unique_id=student)
                contain.save()
                flag = 1
                break
        if flag == 0:
            group = Group.objects.create(course_id=course, level=student.level)
            group.save()
            contain = Contain.objects.create(group_id=group, unique_id=student)
            contain.save()


def about(request):
    return render(request, 'epsilon/about.html')


@login_required
def mdashboard(request):
    courses = Course.objects.all()
    career = Career.objects.all()
    context = {'courses': courses, 'career': career}
    return render(request, "epsilon/mentor_dashboard.html", context)


@login_required
def manage(request):
    user = request.user
    courses = Course.objects.filter(Q(pk__in=Manage.objects.filter(Q(mentor_id__in=Mentor.objects.filter(Q(mentor_id__in=ExtraInfo.objects.filter(Q(user=user)))))).values('course_id_id')))
    context = {'courses': courses}
    return render(request, "epsilon/managecourses.html", context)


@login_required
def edittopic(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, "epsilon/editsubtopic.html", context)


@login_required
def editquiz(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, "epsilon/editquiz.html", context)


@login_required
def editcourse(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, "epsilon/editcourse.html", context)


@login_required
def loggedout(request):
    logout(request)
    return redirect('/epsilon')


''' RECOMMENDER '''

# for recommender
import numpy as np
import scipy.stats
import scipy.spatial
from sklearn.cross_validation import KFold
import random
from sklearn.metrics import mean_squared_error
from math import sqrt
import math
import warnings
import sys


def recommender_related(rec_for):
    users = 27  # TODO: Change this to total number of students in the db
    items = 19  # TODO: Change this to total number of courses in the db
    recommend_data = readingFile("C:\\Users\\arsha\\Documents\\GitHub\\IntelliStudy\\epsilon\\grades.csv") # TODO: Change this address get grades from scores and store into a csv and avg based on courses
    high1, high2, low1, low2 = predictRating(recommend_data, users, items, rec_for)
    # highs are easiest for him to score high
    # lows will be hard for him to score high
    return HttpResponse("Done Recommendation\n High:" + str(high1) + " " + str(high2) + "\n LOW: " + str(low1) + " " + str(low2))

def readingFile(filename):
    f = open(filename,"r")
    data = []
    for row in f:
        r = row.split(',')
        e = [int(r[0]), int(r[1]), int(r[2])]
        data.append(e)
    return data

def predictRating(recommend_data, users, items, rec_for):

    M, sim_user = crossValidation(recommend_data, users, items)
    pred_low1 = 10
    pred_low2 = 10
    pred_high1 = 0
    pred_high2 = 0
    f = open("C:\\Users\\arsha\\Documents\\GitHub\\IntelliStudy\\epsilon\\toBeGraded.csv","r")  # TODO: Change this address to the courses not enrolled
    #f = open(sys.argv[2],"r")
    toBeRated = {"user":[], "item":[]}
    for row in f:
        r = row.split(',')
        toBeRated["item"].append(int(r[1]))
        toBeRated["user"].append(rec_for)

    f.close()

    pred_rate = []

    #fw = open('result1.csv','w')
    fw_w = open('C:\\Users\\arsha\\Documents\\GitHub\\IntelliStudy\\epsilon\\result1.csv','w')  # TODO: Change this to return the results

    l = len(toBeRated["user"])
    for e in range(l):
        user = toBeRated["user"][e]
        item = toBeRated["item"][e]

        pred = 5.0

        #user-based
        if np.count_nonzero(M[user-1]):
            sim = sim_user[user-1]
            ind = (M[:,item-1] > 0)
            #ind[user-1] = False
            normal = np.sum(np.absolute(sim[ind]))
            if normal > 0:
                pred = np.dot(sim,M[:,item-1])/normal

        if pred < 0:
            pred = 0

        if pred > 10:
            pred = 10

        pred_rate.append(pred)

        if(pred<pred_low1):
            pred_low1=pred
            low1 = item
        elif (pred<pred_low2):
            pred_low2=pred
            low2 = item

        if (pred > pred_high1):
            pred_high1 = pred
            high1 = item
        elif (pred > pred_high2):
            pred_high2 = pred
            high2 = item

        print (str(user) + "," + str(item) + "," + str(pred))
        #fw.write(str(user) + "," + str(item) + "," + str(pred) + "\n")
        fw_w.write(str(item) + "," + str(pred) + "\n")                      #   this is how you make csv

    #fw.close()
    fw_w.close()
    return high1, high2, low1, low2

def crossValidation(data, users, items):
    k_fold = KFold(n=len(data), n_folds=10)

    Mat = np.zeros((users,items))
    for e in data:
        Mat[e[0]-1][e[1]-1] = e[2]

    sim_user_cosine, sim_user_jaccard, sim_user_pearson = similarity_user(Mat, users, items)

    rmse_cosine = []
    rmse_jaccard = []
    rmse_pearson = []

    for train_indices, test_indices in k_fold:
        train = [data[i] for i in train_indices]
        test = [data[i] for i in test_indices]

        M = np.zeros((users,items))

        for e in train:
            M[e[0]-1][e[1]-1] = e[2]

        true_rate = []
        pred_rate_cosine = []
        pred_rate_jaccard = []
        pred_rate_pearson = []

        for e in test:
            user = e[0]
            item = e[1]
            true_rate.append(e[2])

            pred_cosine = 5.0
            pred_jaccard = 5.0
            pred_pearson = 5.0

            #user-based
            if np.count_nonzero(M[user-1]):
                sim_cosine = sim_user_cosine[user-1]
                sim_jaccard = sim_user_jaccard[user-1]
                sim_pearson = sim_user_pearson[user-1]
                ind = (M[:,item-1] > 0)
                #ind[user-1] = False
                normal_cosine = np.sum(np.absolute(sim_cosine[ind]))
                normal_jaccard = np.sum(np.absolute(sim_jaccard[ind]))
                normal_pearson = np.sum(np.absolute(sim_pearson[ind]))
                if normal_cosine > 0:
                    pred_cosine = np.dot(sim_cosine,M[:,item-1])/normal_cosine

                if normal_jaccard > 0:
                    pred_jaccard = np.dot(sim_jaccard,M[:,item-1])/normal_jaccard

                if normal_pearson > 0:
                    pred_pearson = np.dot(sim_pearson,M[:,item-1])/normal_pearson

            if pred_cosine < 0:
                pred_cosine = 0

            if pred_cosine > 10:
                pred_cosine = 10

            if pred_jaccard < 0:
                pred_jaccard = 0

            if pred_jaccard > 10:
                pred_jaccard = 10

            if pred_pearson < 0:
                pred_pearson = 0

            if pred_pearson > 10:
                pred_pearson = 10

            print (str(user) + "\t" + str(item) + "\t" + str(e[2]) + "\t" + str(pred_cosine) + "\t" + str(pred_jaccard) + "\t" + str(pred_pearson))
            pred_rate_cosine.append(pred_cosine)
            pred_rate_jaccard.append(pred_jaccard)
            pred_rate_pearson.append(pred_pearson)

        rmse_cosine.append(sqrt(mean_squared_error(true_rate, pred_rate_cosine)))
        rmse_jaccard.append(sqrt(mean_squared_error(true_rate, pred_rate_jaccard)))
        rmse_pearson.append(sqrt(mean_squared_error(true_rate, pred_rate_pearson)))

        print (str(sqrt(mean_squared_error(true_rate, pred_rate_cosine))) + "\t" + str(sqrt(mean_squared_error(true_rate, pred_rate_jaccard))) + "\t" + str(sqrt(mean_squared_error(true_rate, pred_rate_pearson))))
        #raw_input()

    #print sum(rms) / float(len(rms))
    rmse_cosine = sum(rmse_cosine) / float(len(rmse_cosine))
    rmse_pearson = sum(rmse_pearson) / float(len(rmse_pearson))
    rmse_jaccard = sum(rmse_jaccard) / float(len(rmse_jaccard))

    print (str(rmse_cosine) + "\t" + str(rmse_jaccard) + "\t" + str(rmse_pearson))

    f_rmse = open("rmse_user.txt","w")
    f_rmse.write(str(rmse_cosine) + "\t" + str(rmse_jaccard) + "\t" + str(rmse_pearson) + "\n")

    rmse = [rmse_cosine, rmse_jaccard, rmse_pearson]
    req_sim = rmse.index(min(rmse))

    print (req_sim)
    f_rmse.write(str(req_sim))
    f_rmse.close()

    if req_sim == 0:
        sim_mat_user = sim_user_cosine

    if req_sim == 1:
        sim_mat_user = sim_user_jaccard

    if req_sim == 2:
        sim_mat_user = sim_user_pearson

    #predictRating(Mat, sim_mat_user)
    return Mat, sim_mat_user

def similarity_user(data, users, items):
    user_similarity_cosine = np.zeros((users,users))
    user_similarity_jaccard = np.zeros((users,users))
    user_similarity_pearson = np.zeros((users,users))
    for user1 in range(users):
        print (user1)
        for user2 in range(users):
            if np.count_nonzero(data[user1]) and np.count_nonzero(data[user2]):
                user_similarity_cosine[user1][user2] = 1-scipy.spatial.distance.cosine(data[user1],data[user2])
                user_similarity_jaccard[user1][user2] = 1-scipy.spatial.distance.jaccard(data[user1],data[user2])
                try:
                    if not math.isnan(scipy.stats.pearsonr(data[user1],data[user2])[0]):
                        user_similarity_pearson[user1][user2] = scipy.stats.pearsonr(data[user1],data[user2])[0]
                    else:
                        user_similarity_pearson[user1][user2] = 0
                except:
                    user_similarity_pearson[user1][user2] = 0
    return user_similarity_cosine, user_similarity_jaccard, user_similarity_pearson