from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Course, CustomUser, Department, Teacher
import uuid

from .EmailBackend import EmailBackend

# Create your views here.


def LoginUser(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('email')
            password = request.POST.get('password')
            user = EmailBackend.authenticate(request,
                                             username=username, password=password)

            if user is not None:
                login(request, user)
                user_type = user.user_type
                if user_type == '1':
                    return redirect('/uni-admin/')
                elif user_type == '2':
                    return redirect('/teacher/')
                elif user_type == '3':
                    return redirect('/student/')
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('/')
        else:
            print('not post')
    except:
        print('error')
        pass

    return render(request, 'login.html')


def register(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'register.html')


def Logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/')
def ADMIN(request):
    return render(request, 'admin.html')


@login_required(login_url='/')
def EDITPROFILE(request):
    context = {}
    try:
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        context = {
            'user': user
        }

        if request.method == 'POST':
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            profile_pic = request.FILES.get('profile_image')

            user = CustomUser.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name

            if(password != '' and password != None):
                user.set_password(password)

            if(profile_pic != '' and profile_pic != None):
                user.profile_pic = profile_pic

            user.save()

            context = {
                'user': user
            }

            messages.error(request, 'Data updated Successfully')
            redirect('/edit-profile/')

        else:
            print('not post')

    except Exception as e:
        print(e)
        pass

    return render(request, 'edit-profile.html', context)


@login_required(login_url='/')
def ADD_TEACHER(request):
    route = '/add-teacher/'
    context = {}
    try:
        departments = Department.objects.all()
        context = {
            'departments': departments
        }

        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            profile_pic = request.FILES.get('profile_pic')

            gender = request.POST.get('gender')

            short_code = request.POST.get('short_code')
            qualifications = request.POST.get('qualifications')
            designations = request.POST.get('designations')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            department_id = request.POST.get('department')

            if(department_id == '' or department_id == None):
                messages.error(request, 'Department is required')
                return redirect(route)

            if(gender == '' or gender == None):
                messages.error(request, 'Department is required')
                return redirect(route)

            if(Teacher.objects.filter(short_code=short_code).exists()):
                messages.warning(request, 'Short code already exists')
                return redirect(route)

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
                user_type='2',
            )

            user.set_password(password)
            user.save()

            department = Department.objects.get(id=department_id)

            teacher = Teacher(
                admin=user,
                short_code=short_code,
                qualifications=qualifications,
                designations=designations,
                address=address,
                phone=phone,
                department=department,
                gender=gender
            )

            teacher.save()

            messages.error(request, 'Data updated Successfully')
            redirect(route, context)

        else:

            redirect(route, context)

    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        return redirect(route)

    return render(request, 'add-teacher.html', context)


@login_required(login_url='/')
def ADD_COURSE(request):
    # course_token
    def get_unique_code():
        course_token = str(uuid.uuid4())[:8]
        is_exists = Course.objects.filter(course_token=course_token).exists()

        if(is_exists):
            get_unique_code()
        else:
            return course_token

    route = '/add-course/'
    context = {}
    try:
        departments = Department.objects.all()
        users = CustomUser.objects.filter(user_type='2')

        context = {
            'departments': departments,
            'teachers': users
        }

        if request.method == 'POST':
            course_image = request.FILES.get('course_image')
            course_name = request.POST.get('course_name')
            course_code = request.POST.get('course_code')
            course_description = request.POST.get('course_description')
            course_token = get_unique_code()

            # course_teacher_id = request.POST.get('course_teacher')

            department_id = request.POST.get('department')

            # print(course_teacher_id, department_id)

            if(department_id == '' or department_id == None):
                messages.error(request, 'Department is required')
                return redirect(route)

            # if(course_teacher_id == '' or course_teacher_id == None):
            #     messages.error(request, 'Course teacher is required')
            #     return redirect(route)

            if(Course.objects.filter(course_code=course_code).exists()):
                messages.warning(request, 'Course already exists')
                return redirect(route)

            if(Course.objects.filter(course_name=course_name).exists()):
                messages.warning(request, 'Course already exists')
                return redirect(route)

            department = Department.objects.get(id=department_id)

            # teacher = CustomUser.objects.get(id=course_teacher_id)

            # if(Course.objects.filter(course_teacher=teacher).exists() and Course.objects.filter(course_code=course_code).exists()):
            #     messages.warning(
            #         request, 'Course already asssgned to this teacher')
            #     return redirect(route)
            if(Course.objects.filter(department=department).exists() and Course.objects.filter(course_code=course_code).exists()):
                messages.warning(
                    request, 'Course already asssgned to this department')
                return redirect(route)

            course = Course(
                course_code=course_code,
                course_name=course_name,
                course_description=course_description,
                course_image=course_image,
                course_token=course_token,
                # course_teacher=teacher,
                department=department
            )

            course.save()

            messages.error(
                request, 'Course add Successfully\nCourse Token: ' + ' ' + course_token)
            redirect(route, context)

        else:

            redirect(route, context)

    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        return redirect(route)

    return render(request, 'add-course.html', context)
