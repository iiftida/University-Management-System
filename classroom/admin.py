from django.contrib import admin
from .models import StudentCourses, Assignment, Course, CustomUser, Department, Notice, Student, Submission, Teacher
from django.contrib.auth.admin import UserAdmin


class UserModel(UserAdmin):
    list_display = ['username', 'user_type']

    # Register your models here.
admin.site.register(CustomUser, UserModel)
admin.site.register(Department)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Notice)
admin.site.register(Assignment)
admin.site.register(Student)
admin.site.register(StudentCourses)
admin.site.register(Submission)
