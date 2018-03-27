from django.contrib import admin

from .models import (ExtraInfo, Student, Mentor, Course, Content, Question, Option, Career, Has,
                    Enroll, Score, Group, Contain, Manage, Message, Peer, Progress, File)

admin.site.register(ExtraInfo)
admin.site.register(Student)
admin.site.register(Mentor)
admin.site.register(Course)
admin.site.register(Content)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Career)
admin.site.register(Has)
admin.site.register(Enroll)
admin.site.register(Score)
admin.site.register(Group)
admin.site.register(Contain)
admin.site.register(Manage)
admin.site.register(Message)
admin.site.register(Peer)
admin.site.register(Progress)
admin.site.register(File)
