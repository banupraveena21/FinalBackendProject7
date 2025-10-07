from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Attendance, SalarySlip
from .forms import EmployeeForm, AttendanceForm
from django.db.models import Count
from django.http import HttpResponse
from xhtml2pdf import pisa
import openpyxl

def dashboard(request):
    total_employees = Employee.objects.count()
    total_attendance = Attendance.objects.count()
    total_salary_slips = SalarySlip.objects.count()
    
    return render(request, 'payroll_app/dashboard.html', {
        'total_employees': total_employees,
        'total_attendance': total_attendance,
        'total_salary_slips': total_salary_slips,
    })

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'payroll_app/employee_list.html', {'employees': employees})

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'payroll_app/base_form.html', {'form': form, 'title': 'Add Employee'})

def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, instance=employee)
    if form.is_valid():
        form.save()
        return redirect('employee_list')
    return render(request, 'payroll_app/base_form.html', {'form': form, 'title': 'Edit Employee'})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'payroll_app/confirm_delete.html', {'employee': employee})

def attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance')
    else:
        form = AttendanceForm()
    records = Attendance.objects.all()
    return render(request, 'payroll_app/attendance.html', {'form': form, 'records': records})

def generate_salary(request):
    salary_slips = []
    employees = Employee.objects.all()

    for emp in employees:
        presents = Attendance.objects.filter(employee=emp, status='Present').count()
        total_salary = presents * (emp.salary / 30)  # salary based on per day
        slip = SalarySlip.objects.create(employee=emp, month='October 2025', total_present_days=presents, total_salary=total_salary)
        salary_slips.append(slip)

    return render(request, 'payroll_app/salary_slip.html', {'slips': salary_slips})

def export_pdf(request):
    slips = SalarySlip.objects.all()
    return render(request, 'payroll_app/export_salary.html', {'slips': slips})

def export_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Employee', 'Month', 'Days Present', 'Total Salary'])

    for slip in SalarySlip.objects.all():
        ws.append([slip.employee.name, slip.month, slip.total_present_days, float(slip.total_salary)])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=salary.xlsx'
    wb.save(response)
    return response
