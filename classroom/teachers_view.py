from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .EmailBackend import EmailBackend
from .models import Assignment, Course, CustomUser, Department, Notice, Submission, Teacher


@login_required(login_url='/')
def TEACHER(request):
    route = '/teacher/'
    context = {}
    try:
        user = CustomUser.objects.get(id=request.user.id)
        courses = Course.objects.filter(course_teacher=user)
        context = {
            'courses': courses,
            'user': user,
        }
        print(courses)
    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        pass

    return render(request, 'teacher.html', context)


@login_required(login_url='/')
def TEACHER_COURSE(request):
    route = '/teacher-home/'
    context = {}
    try:
        # user = CustomUser.objects.get(id=request.user.id)
        # courses = Course.objects.filter(course_teacher=user)
        course_id = request.GET.get('course_id')
        teacher_id = request.GET.get('teacher_id')

        course_id = request.GET.get('course_id')
        user = CustomUser.objects.get(id=teacher_id)
        course = Course.objects.get(id=course_id)

        context = {
            'course_id': course_id,
            'teacher_id': teacher_id,
            'user': user,
            'course': course,
        }

    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        pass

    return render(request, 'teacher-home.html', context)


@login_required(login_url='/')
def ADD_NOTICE(request):
    route = '/add-notice/'
    context = {}

    try:
        # user = CustomUser.objects.get(id=request.user.id)
        # courses = Course.objects.filter(course_teacher=user)
        course_id = request.GET.get('course_id')
        teacher_id = request.GET.get('teacher_id')
        print(course_id)

        context = {
            'course_id': course_id,
            'teacher_id': teacher_id,
        }

        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            print(course)
            teacher = CustomUser.objects.get(id=teacher_id)

            notice_title = request.POST.get('notice_title')
            notice_description = request.POST.get('notice_description')
            notice_image = request.FILES.get('notice_image')
            notice_file = request.FILES.get('notice_file')

            if(notice_title == '' or notice_title == None or notice_description == '' or notice_description == None):
                messages.error(request, 'Please fill all the fields')
                return redirect(route, context)

            notice = Notice(
                course=course,
                teacher=teacher,
                notice_title=notice_title,
                notice_description=notice_description,
                notice_image=notice_image,
                notice_file=notice_file,
            )

            notice.save()

            messages.error(request, 'Notice added Successfully')

            URI = '/add-notice/?course_id=' + \
                str(course_id) + '&teacher_id=' + str(teacher_id)

            context = {
                'course': course,
                'course_id': course_id,
                'teacher_id': teacher_id,
            }
            return redirect(URI, context)

    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        pass

    return render(request, 'add-notice.html', context)


@login_required(login_url='/')
def ADD_ASSIGNMENT(request):
    route = '/add-assignment/'
    context = {}

    try:
        # user = CustomUser.objects.get(id=request.user.id)
        # courses = Course.objects.filter(course_teacher=user)
        course_id = request.GET.get('course_id')
        teacher_id = request.GET.get('teacher_id')
        print(course_id)

        context = {
            'course_id': course_id,
            'teacher_id': teacher_id,
        }

        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            print(course)
            teacher = CustomUser.objects.get(id=teacher_id)

            assignment_title = request.POST.get('assignment_title')
            assignment_description = request.POST.get('assignment_description')
            assignment_image = request.FILES.get('assignment_image')
            assignment_file = request.FILES.get('assignment_file')
            assignment_submission_date = request.POST.get(
                'assignment_submission_date')

            print(assignment_submission_date, assignment_description,
                  assignment_title, assignment_image, assignment_file)

            if(assignment_title == '' or assignment_title == None or assignment_description == '' or assignment_description == None or assignment_submission_date == '' or assignment_submission_date == None):
                messages.error(request, 'Please fill all the fields')
                return redirect(route, context)

            notice = Assignment(
                course=course,
                teacher=teacher,
                assignment_title=assignment_title,
                assignment_description=assignment_description,
                assignment_image=assignment_image,
                assignment_file=assignment_file,
                assignment_submission_date=assignment_submission_date
            )

            notice.save()

            messages.error(request, 'Assignment added Successfully')

            URI = '/add-assignment/?course_id=' + \
                str(course_id) + '&teacher_id=' + str(teacher_id)

            context = {
                'course': course,
                'course_id': course_id,
                'teacher_id': teacher_id,
            }
            return redirect(URI, context)

    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        pass

    return render(request, 'add-assignment.html', context)


@login_required(login_url='/')
def GETSUBMISSIONS(request):
    context = {}

    try:
        course_id = request.GET.get('course_id')

        course = Course.objects.get(id=course_id)
        assignment = Assignment.objects.get(course=course)
        submissions = Submission.objects.filter(
            assignment=assignment)

        print(submissions)

        context = {
            'course': course,
            'submissions': submissions,
        }

    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        pass

    return render(request, 'submissions.html', context)


@login_required(login_url='/')
def ADDREMARKS(request):
    context = {}

    try:
        if request.method == 'POST':
            submission_id = request.GET.get('submission_id')
            is_examined = True
            submisssion_thoughts = request.POST.get('submisssion_thoughts')
            submisssion_marks = request.POST.get('submisssion_marks')
            submissions = Submission.objects.get(id=submission_id)
            if(submissions.is_examined):
                messages.error(request, 'Already examined')
                return redirect('/add-remarks/?submission_id=' + str(submission_id))
            else:
                submissions.is_examined = is_examined
                submissions.submisssion_thoughts = submisssion_thoughts
                submissions.submisssion_marks = submisssion_marks
                submissions.save()
                messages.error(request, 'Remarks added Successfully')
                return redirect('/add-remarks/?submission_id=' + str(submission_id))

    except Exception as e:
        print(e)
        messages.error(request, 'Error')
        pass

    return render(request, 'remark.html', context)
