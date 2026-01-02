from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Teacher, Student , Attendance
from django.contrib import messages


User = get_user_model()

def home(request):
    return render(request, 'mystudent/home.html')


def register(request):
    if request.method == 'POST':
        
        user = User.objects.create_user(
            first_name=request.POST['firstname'],
            last_name=request.POST['lastname'],
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password'],
            usertype='Student',
            is_active=True  
        )

        
        Student.objects.create(
            Student_id=user,
            address=request.POST['address'],
            Ph_no=request.POST['ph_no'],
            guardian=request.POST['guardian']
        )

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'mystudent/register.html')


def logins(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('admins')
            elif user.usertype == 'Teacher':
                return redirect('teacher_home')
            else:
                return redirect('student_home')

        messages.error(request, "Invalid username or password")

    return render(request, 'mystudent/logins.html')


@login_required
def admins(request):
    if not request.user.is_superuser:
        return redirect('login')
    return render(request, 'mystudent/admins.html')


@login_required
def teacher_home(request):
    return render(request, 'mystudent/teacher.html')


@login_required
def student_home(request):
    return render(request, 'mystudent/student.html')


@login_required
def addteacher(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            first_name=request.POST['firstname'],
            last_name=request.POST['lastname'],
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password'],
            usertype='Teacher',
            is_active=False,
            is_staff=True
        )

        Teacher.objects.create(
            Teacher_id=user,
            address=request.POST['address'],
            Ph_no=request.POST['ph_no'],
            salary=request.POST['salary'],
            experience=request.POST['experience']
        )
        messages.success(request, "Teacher added successfully. Awaiting admin approval.")

    return render(request, 'mystudent/addteacher.html')


@login_required
def viewteacher(request):
    teachers = Teacher.objects.all()
    return render(request, 'mystudent/viewteacher.html', {'view': teachers})


@login_required
def approveteacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    teacher.Teacher_id.is_active = True
    teacher.Teacher_id.save()
    return redirect('viewteacher')


@login_required
def deleteteacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    teacher.Teacher_id.delete()
    teacher.delete()
    return redirect('viewteacher')


@login_required
def addstudent(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            first_name=request.POST['firstname'],
            last_name=request.POST['lastname'],
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password'],
            usertype='Student',
            is_active=True
        )

        Student.objects.create(
            Student_id=user,
            address=request.POST['address'],
            Ph_no=request.POST['ph_no'],
            guardian=request.POST['guardian']
        )
        return HttpResponse("Student added successfully")

    return render(request, 'mystudent/addstudent.html')


@login_required
def viewstudent(request):
    students = Student.objects.all()
    return render(request, 'mystudent/viewstudent.html', {'view': students})




@login_required
def deletestudent(request, id):
    student = get_object_or_404(Student, id=id)
    student.Student_id.delete()
    student.delete()
    return redirect('viewstudent')


@login_required
def student_profile(request):
    student = get_object_or_404(Student, Student_id=request.user)
    return render(request, 'mystudent/student_profile.html', {'student': student})
@login_required
def student_profile_by_teacher(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'mystudent/student_profile.html', {'student': student})

@login_required
def teacher_profile(request):
    teacher = get_object_or_404(Teacher, Teacher_id=request.user)
    return render(request, 'mystudent/teacher_profile.html', {'teacher': teacher})

@login_required
def teacher_view_students(request):
    students = Student.objects.all()

    letter = request.GET.get('letter')
    if letter:
        students = students.filter(
            Student_id__first_name__istartswith=letter
        )

    return render(request, 'mystudent/teacher_view_students.html', {
        'students': students
    })



@login_required
def edit_student_profile(request):
    student = get_object_or_404(Student, Student_id=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST['firstname']
        request.user.last_name = request.POST['lastname']
        request.user.email = request.POST['email']
        request.user.save()

        student.address = request.POST['address']
        student.ph_no = request.POST['ph_no']
        student.guardian = request.POST['guardian']
        student.save()

        return redirect('student_profile')

    return render(request, 'mystudent/edit_student_profile.html', {'student': student})

@login_required
def edit_teacher_profile(request):
    teacher = get_object_or_404(Teacher, Teacher_id=request.user)

    if request.method == 'POST':
        # Update User fields
        request.user.first_name = request.POST['firstname']
        request.user.last_name = request.POST['lastname']
        request.user.email = request.POST['email']
        request.user.save()

        # Update Teacher fields
        teacher.address = request.POST['address']
        teacher.Ph_no = request.POST['ph_no']  # ensure this matches your model
        teacher.salary = request.POST['salary']
        teacher.save()

        return redirect('teacher_profile')  # redirect to teacher profile page

    return render(request, 'mystudent/edit_teacher_profile.html', {'teacher': teacher})

def user_logout(request):
    logout(request)
    return redirect('login') 



@login_required
def mark_attendance(request):
    teacher = get_object_or_404(Teacher, Teacher_id=request.user)
    students = Student.objects.all()

    if request.method == 'POST':
        date = request.POST['date']

        for student in students:
            status = request.POST.get(str(student.id))
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={'status': status}
                )

        return redirect('teacher_home')

    return render(request, 'mystudent/mark_attendance.html', {'students': students})

@login_required
def view_attendance(request):
    student = get_object_or_404(Student, Student_id=request.user)
    attendance = Attendance.objects.filter(student=student).order_by('-date')

    return render(request, 'mystudent/view_attendance.html', {'attendance': attendance})
