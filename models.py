from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    usertype=models.CharField(max_length=10)

class Teacher(models.Model):
    Teacher_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True, verbose_name="Address")
    Ph_no = models.CharField(max_length=15, blank=True, verbose_name="Phone Number")  
    salary = models.IntegerField(blank=True, null=True, verbose_name="Salary")
    experience = models.IntegerField(blank=True, null=True, verbose_name="Experience")

    
class Student(models.Model):
    Student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True, verbose_name="Address")
    Ph_no = models.CharField(max_length=15, blank=True, verbose_name="Phone Number")  
    guardian = models.CharField(max_length=50, blank=True, verbose_name="guardian")
        
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[('Present', 'Present'), ('Absent', 'Absent')])
