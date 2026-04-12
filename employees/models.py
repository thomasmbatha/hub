from django.conf import settings
from django.db import models

# Create your models here.
   
# 🔹 Personal and Employment information

class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    date_of_birth = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    home_address = models.TextField(blank=True)

    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, default="Unassigned")
    job_title = models.CharField(max_length=100, default="Employee")
    shift = models.CharField(max_length=50, default="Day")
    manager = models.CharField(max_length=100, default="Not Assigned")
    employment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.employee_id


# 🔹 Banking details
class BankingDetail(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=30)
    bank_name = models.CharField(max_length=100)
    branch_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.employee.first_name} Banking"


# 🔹 Emergency contact information
class EmergencyContact(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    contact_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.contact_name} ({self.employee.first_name})"