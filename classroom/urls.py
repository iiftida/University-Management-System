from django.urls import path

from . import views
from . import teachers_view
from . import student_view
from . import admin_views

urlpatterns = [
    path('', views.LoginUser, name='LoginUser'),
    path('register/', student_view.REGISTER, name='register'),
    path('uni-admin/', views.ADMIN, name='uni-admin'),
    path('logout/', views.Logout, name='logout'),
    path('edit-profile/', views.EDITPROFILE, name='edit-profile'),
    path('add-teacher/', views.ADD_TEACHER, name='add-teacher'),
    path('add-course/', views.ADD_COURSE, name='add-course'),
    path('teacher/', teachers_view.TEACHER, name='teacher'),
    path('student/', student_view.STUDENT, name='student'),
    path('teacher-home/', teachers_view.TEACHER_COURSE, name='teacher-home'),
    path('add-notice/', teachers_view.ADD_NOTICE, name='add-notice'),
    path('submissions/', teachers_view.GETSUBMISSIONS, name='submissions'),
    path('add-assignment/', teachers_view.ADD_ASSIGNMENT, name='add-assignment'),
    path('add-department/', admin_views.ADD_DEPARTMENT, name='add-department'),
    path('assign-course/', admin_views.ASSIGN_COURSES, name='assign-course'),
    path('join-class/', student_view.JOINCLASS, name='join-class'),
    path('student-home/', student_view.STUDENTHOME, name='student-home'),
    path('subject-assignment/', student_view.ALLASSIGNMENTS,
         name='subject-assignment'),
    path('subject-notice/', student_view.NOTICES, name='subject-notice'),
    path('submit-assignment/', student_view.SUBMITASSSIGNMENTS,
         name='submit-assignment'),
    path('add-remarks/', teachers_view.ADDREMARKS, name='add-remarks'),


]
