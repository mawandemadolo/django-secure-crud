from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .forms import EmployeeForm
from django.shortcuts import redirect
from .models import Employee
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.exceptions import ValidationError


# Create view.
@login_required
@never_cache
@csrf_protect
def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee created successfully')
            return redirect('list')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = EmployeeForm() 
    return render(request, 'create.html', {'form':form})


# list view
@login_required
@never_cache
def employee_list(request):
    employee = Employee.objects.all()
    return render(request, 'list.html', {'employees':employee})

# updpate view
@login_required
@never_cache
@csrf_protect
def update_employee(request, pk):
    try:
        pk = int(pk)
        if pk <= 0:
            raise Http404
    except (ValueError, TypeError):
        raise Http404
    
    employee = get_object_or_404(Employee, id=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully')
            return redirect('list')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'update.html', {'form':form})

# delete view
@login_required
@never_cache
@csrf_protect
def delete_employee(request, pk):
    try:
        pk = int(pk)
        if pk <= 0:
            raise Http404
    except (ValueError, TypeError):
        raise Http404
    
    employee = get_object_or_404(Employee, id=pk)
    if request.method == "POST":
        employee.delete()
        messages.success(request, 'Employee deleted successfully')
        return redirect('list')
    raise Http404