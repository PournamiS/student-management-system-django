"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from mystudent import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.logins, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('admins/', views.admins, name='admins'),

    path('teacher/', views.teacher_home, name='teacher_home'),
    path('student/', views.student_home, name='student_home'),

    path('addteacher/', views.addteacher, name='addteacher'),
    path('viewteacher/', views.viewteacher, name='viewteacher'),
    path('approveteacher/<int:id>/', views.approveteacher, name='approveteacher'),
    path('deleteteacher/<int:id>/', views.deleteteacher, name='deleteteacher'),

    path('addstudent/', views.addstudent, name='addstudent'),
    path('viewstudent/', views.viewstudent, name='viewstudent'),
    path('deletestudent/<int:id>/', views.deletestudent, name='deletestudent'),
    path('teacherviewstudent/', views.teacher_view_students, name='teacher_view_students'),

    path('studentprofile/', views.student_profile, name='student_profile'),
    path('studentprofilebyteacher/<int:id>/', views.student_profile_by_teacher, name='student_profile_by_teacher'),
    path('teacherprofile/', views.teacher_profile, name='teacher_profile'),
    path('editstudentprofile/', views.edit_student_profile, name='edit_student_profile'),
    path('editteacherprofile/', views.edit_teacher_profile, name='edit_teacher_profile'),
    path('logout/', views.user_logout, name='logout'),
    path('markattendance/', views.mark_attendance, name='mark_attendance'),
    path('viewattendance/', views.view_attendance, name='view_attendance'),


]
