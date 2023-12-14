from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .EmailBackend import EmailBackend
from .models import Assignment, Course, CustomUser, Department, Notice, Teacher


@login_required(login_url='/')
def ADD_DEPARTMENT(request):
    route = '/add-department/'
    context = {}
    try:
        if(request.method == 'POST'):
            department_name = request.POST.get('department_name')
            department_description = request.POST.get('department_description')
            department_code = request.POST.get('department_code')
            department_image = request.POST.get('department_image')
            if(department_name == '' or department_name == None):
                messages.error(request, 'Department name is required')
                return redirect(route)
            if(department_code == '' or department_code == None):
                messages.error(request, 'Department code is required')
                return redirect(route)

            is_duplicate_code = Department.objects.filter(
                department_code=department_code).exists()

            if(is_duplicate_code):
                messages.error(request, 'Department code already exists')
                return redirect(route)

            department = Department(
                department_name=department_name,
                department_description=department_description,
                department_code=department_code,
                department_image=department_image,
            )
            department.save()
            messages.error(request, 'Department Added successfully')
            return redirect(route)

    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        pass

    return render(request, 'add-department.html', context)


def ASSIGN_COURSES(request):
    route = '/assign-course/'
    context = {}
    try:
        courses = Course.objects.all()
        teachers = CustomUser.objects.filter(user_type='2')

        context = {
            'courses': courses,
            'teachers': teachers,
        }

        if(request.method == 'POST'):
            course_id = request.POST.get('course_id')
            teacher_id = request.POST.get('teacher_id')
            print(course_id)

            course = Course.objects.get(id=course_id)
            teacher = CustomUser.objects.get(id=teacher_id)

            if(course_id == None or course_id == ''):
                messages.error(request, 'Course  must be selected')
                return redirect(route)

            if(teacher_id == None or teacher_id == ''):
                messages.error(request, 'Teacher teacher must be selected')
                return redirect(route)

            if(course.course_teacher != None):
                messages.error(
                    request, 'Teacher already assigned to this course')
                return redirect(route)

            if(course.course_teacher == teacher):
                messages.error(
                    request, 'This Teacher is already assigned to this course')
                return redirect(route)

            course = Course.objects.get(id=course_id)
            course.course_teacher = teacher
            course.save()

            messages.error(
                request, 'Department Added successfully, Course Token is ' + str(course.course_token))
            return redirect(route)

    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        pass

    return render(request, 'assign-course.html', context)
