from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeForm
from django.utils import timezone

def profile(request):
    employee = Employee.objects.filter(user=request.user).first()

    return render(request, "employees/profile.html", {
        "employee": employee
    })


def edit_profile(request):
    return render(request, "employees/edit_profile.html")

@login_required
def create_profile(request):
    if request.method == 'POST':

        Employee.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            date_of_birth=request.POST.get('date_of_birth') or None,
            contact_number=request.POST.get('contact_number'),
            home_address=request.POST.get('home_address'),
            employee_id=f"EMP{request.user.id:04d}",
            department=request.POST.get('department'),
            job_title=request.POST.get('job_title'),
            shift=request.POST.get('shift'),
            manager=request.POST.get('manager'),
            employment_date=timezone.now().date()
        )

        return redirect('profile')

    return render(request, 'employees/create_profile.html')


@login_required
def edit_profile(request):
    employee = request.user.employee_profile

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employees/edit_profile.html', {
        'form': form
    })