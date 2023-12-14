
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .EmailBackend import EmailBackend
from .models import (Assignment, Course, CustomUser, Department, Notice,
                     StudentCourses, Submission, Teacher)


@login_required(login_url='/')
def STUDENT(request):
    route = '/student/'
    context = {}
    try:
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        studen_data = StudentCourses.objects.filter(student=user)
        courses = []
        for data in studen_data:
            courses.append(data.course)

        context = {
            'courses': courses,
            'user': user,
        }
        print(courses)
    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        return redirect(route)

    return render(request, 'student.html', context)


def REGISTER(request):
    route = '/register/'
    context = {}
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            profile_pic = request.FILES.get('profile_pic')

            if(CustomUser.objects.filter(username=username).exists()):
                messages.warning(request, 'Username already exists')
                return redirect(route)

            if(CustomUser.objects.filter(email=email).exists()):
                messages.warning(request, 'Email is taken')
                return redirect(route)

            user = CustomUser(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                profile_pic=profile_pic,
                user_type='3',
            )

            user.set_password(password)
            user.save()

            messages.error(request, 'Register Successfull please login')
            return redirect(route, context)

    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        return redirect(route)

    return render(request, 'register.html', context)


@login_required(login_url='/')
def JOINCLASS(request):
    route = '/join-class/'
    context = {}
    try:
        if request.method == 'POST':
            token = request.POST.get('token')
            user_id = request.GET.get('user_id')

            is_token_valid = Course.objects.filter(course_token=token).exists()
            print(is_token_valid)

            if(is_token_valid == False):
                messages.error(request, 'Course does not exists')
                return redirect('/join-class/?user_id='+'' + user_id)

            course = Course.objects.get(course_token=token)
            student = CustomUser.objects.get(id=user_id)

            is_already_joined = StudentCourses.objects.filter(
                course=course, student=student).exists()

            print(is_already_joined)

            if(is_already_joined):
                messages.error(request, 'You are already joined')
                return redirect('/join-class/?user_id='+'' + user_id)

            student_course = StudentCourses(
                course=course,
                student=student,
            )

            student_course.save()

            messages.error(request, 'Register Successfull please login')
            return redirect('/join-class/?user_id='+'' + user_id, context)

    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        return redirect(route)

    return render(request, 'join-class.html', context)


@login_required(login_url='/')
def STUDENTHOME(request):
    route = '/student-home/'
    context = {}
    try:
        if(request.method == 'GET'):
            user_id = request.GET.get('user_id')
            course_id = request.GET.get('course_id')
            user = CustomUser.objects.get(id=user_id)
            course = Course.objects.get(id=course_id)
            context = {
                'user': user,
                'course': course,
            }

    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        return redirect(route)

    return render(request, 'student-home.html', context)


@login_required(login_url='/')
def ALLASSIGNMENTS(request):
    route = '/subject-assignment/'
    context = {}
    try:
        if(request.method == 'GET'):
            user_id = request.GET.get('user_id')
            course_id = request.GET.get('course_id')
            user = CustomUser.objects.get(id=user_id)
            course = Course.objects.get(id=course_id)
            assignments = Assignment.objects.filter(course=course)
            print(assignments)
            context = {
                'user': user,
                'assignments': assignments,
            }

    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        return redirect(route)

    return render(request, 'subject-assignment.html', context)


@login_required(login_url='/')
def NOTICES(request):
    route = '/subject-notice/'
    context = {}
    try:
        if(request.method == 'GET'):
            course_id = request.GET.get('course_id')
            course = Course.objects.get(id=course_id)
            notices = Notice.objects.filter(course=course)
            context = {
                'notices': notices,
            }

    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        return redirect(route)

    return render(request, 'subject-notice.html', context)


@login_required(login_url='/')
def SUBMITASSSIGNMENTS(request):
    route = '/submit-assignment/'
    context = {}
    try:
        if(request.method == 'GET'):
            user_id = request.GET.get('user_id')
            asssignment_id = request.GET.get('assignment_id')
            assignment = Assignment.objects.get(id=asssignment_id)
            user = CustomUser.objects.get(id=user_id)

            context = {
                'assignment': assignment,
            }

        if(request.method == 'POST'):
            submission_file = request.FILES.get('submission_file')
            user_id = request.GET.get('user_id')
            assignment_id = request.GET.get('assignment_id')
            assignment = Assignment.objects.get(id=assignment_id)
            user = CustomUser.objects.get(id=user_id)
            is_already_submitted = Submission.objects.filter(
                assignment=assignment, student=user).exists()

            if(is_already_submitted):
                messages.error(
                    request, 'You have already submitted this assignment')
                return redirect(route+'?user_id=' + user_id + '&assignment_id=' + assignment_id, context)

            if(submission_file == None or submission_file == ''):
                messages.error(request, 'Please upload file')
                return redirect(route+'?user_id=' + user_id + '&assignment_id=' + assignment_id, context)

            submissions = Submission(
                student=user,
                assignment=assignment,
                submission_file=submission_file,
            )
            submissions.save()
            messages.error(request, 'You have submitted this assignment')

            return redirect(route+'?user_id=' + user_id + '&assignment_id=' + assignment_id, context)

    except Exception as e:
        print(e)
        messages.error(request, 'Error')

    return render(request, 'submit-assignment.html', context)
