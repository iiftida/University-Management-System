from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    USER = (
        (1, 'HOD'),
        (2, 'STUDENT'),
        (3, 'TEACHER'),
    )
    user_type = models.CharField(choices=USER, default=1, max_length=50)
    profile_pic = models.ImageField(upload_to='media/profile')


class Department(models.Model):
    department_name = models.CharField(max_length=100)
    department_code = models.CharField(max_length=100)
    department_image = models.ImageField(upload_to='media/department')
    department_description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name


class Teacher (models.Model):
    admin = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=100)
    short_code = models.CharField(max_length=100)
    qualifications = models.CharField(max_length=100)
    designations = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=100)
    course_description = models.TextField()
    course_image = models.ImageField(upload_to='media/course')
    course_token = models.CharField(max_length=100, unique=True, null=True)
    course_teacher = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name


class Notice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)
    notice_description = models.TextField()
    notice_title = models.CharField(max_length=100)
    notice_image = models.ImageField(upload_to='media/notice')
    notice_file = models.FileField(upload_to='media/notice')
    notice_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notice_title


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)
    assignment_description = models.TextField()
    assignment_title = models.CharField(max_length=100)
    assignment_image = models.ImageField(upload_to='media/assignment')
    assignment_file = models.FileField(upload_to='media/assignment')
    assignment_submission_date = models.CharField(max_length=100)
    assignment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.assignment_title


class Student(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100)


class StudentCourses(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course.course_name + " " + self.student.first_name + " " + self.student.last_name


class Submission(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, null=True)
    is_examined = models.BooleanField(default=False)
    submission_file = models.FileField(upload_to='media/submission', null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    submisssion_thoughts = models.TextField(null=True)
    submisssion_marks = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.assignment.assignment_title + " " + self.student.first_name + " " + self.student.last_name
