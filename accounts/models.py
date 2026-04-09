import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

# OTP Model
class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # OTP is valid for 5 minutes
        return timezone.now() < self.created_at + timedelta(minutes=5)

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))


# Custom User Model
class Account(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('supervisor', 'Supervisor'),
        ('employee', 'Employee'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username
    
# # 🔹 Personal and Employment information
# class Employee(models.Model):
#     # Personal Details
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     date_of_birth = models.DateField()
#     contact_number = models.CharField(max_length=15)
#     home_address = models.TextField()
#     # Employment details
#     employee_id = models.CharField(max_length=10, unique=True)
#     department = models.CharField(max_length=50)
#     job_title = models.CharField(max_length=50)
#     shift = models.CharField(max_length=50)
#     manager = models.CharField(max_length=100)
#     employment_date = models.DateField()

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"


# # 🔹 Banking details
# class BankingDetail(models.Model):
#     employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
#     account_number = models.CharField(max_length=30)
#     bank_name = models.CharField(max_length=100)
#     branch_code = models.CharField(max_length=20)

#     def __str__(self):
#         return f"{self.employee.first_name} Banking"


# # 🔹 Emergency contact information
# class EmergencyContact(models.Model):
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

#     contact_name = models.CharField(max_length=100)
#     relationship = models.CharField(max_length=50)
#     phone_number = models.CharField(max_length=15)

#     def __str__(self):
#         return f"{self.contact_name} ({self.employee.first_name})"