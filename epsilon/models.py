from django.db import models
from django.contrib.auth.models import User


class Constants:
    USER_CHOICES = (
        ('student', 'student'),
        ('mentor', 'mentor'),
    )

    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    CONTENT_TYPE = (
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
    )

    LEVEL = (
        ('beginner', 'beginner'),
        ('intermediate', 'intermediate'),
        ('advanced', 'advanced'),
    )


class ExtraInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=2, choices=Constants.SEX_CHOICES, default='M')
    date_of_birth = models.DateField(null=True)
    profile_picture = models.ImageField(null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=Constants.USER_CHOICES,
                                 default='student')
    job = models.CharField(max_length=40, null=True, blank=True)
    qualification = models.CharField(max_length=40, null=True, blank=True)


class Student:
    id = models.OneToOneField(ExtraInfo, on_delete=models.CASCADE, primary_key=True)
    career_goal = models.CharField(max_length=40, null=True, blank=True)


class Mentor:
    id = models.OneToOneField(ExtraInfo, on_delete=models.CASCADE, primary_key=True)


class Course:
    name = models.CharField(max_length=40)
    description = models.TextField(default='', max_length=1000, blank=True, null=True)


class Question:
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=Constants.LEVEL, default='intermediate')
    question = models.TextField(max_length=4000, null=True, blank=True)
    answer = models.CharField(max_length=100, null=True, blank=True)


class Option:
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.CharField(max_length=100, null=True, blank=True)


class Career:
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)


class Has:
    career_id = models.ForeignKey(Career, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=Constants.LEVEL, default='intermediate')


class Enroll:
    unique_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    feedback = models.TextField(default='', max_length=1000, blank=True, null=True)


class Score:
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE)
    unique_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)


class Group:
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)


class Contain:
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    unique_id = models.ForeignKey(Student, on_delete=models.CASCADE)


class Manage:
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    mentor_id = models.ForeignKey(Mentor, on_delete=models.CASCADE)


class Message:
    message = models.TextField(default='', max_length=8000, blank=True, null=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    unique_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)


class Peer:
    unique_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    question = models.TextField(max_length=4000, null=True, blank=True)
    answer = models.TextField(max_length=4000, null=True, blank=True)


class Progress:
    enroll_id = models.ForeignKey(Enroll, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Constants.CONTENT_TYPE, default='ONGOING')


class Content:
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    level = models.CharField(max_length=20, choices=Constants.LEVEL, default='intermediate')


class File:
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE)
    mentor_id = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    file = FileField()
    name = models.CharField(max_length=100)
