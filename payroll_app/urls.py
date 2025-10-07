from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/edit/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('employees/delete/<int:pk>/', views.employee_delete, name='employee_delete'),
    path('attendance/', views.attendance, name='attendance'),
    path('salary/', views.generate_salary, name='generate_salary'),
    path('salary/export/pdf/', views.export_pdf, name='export_pdf'),
    path('salary/export/excel/', views.export_excel, name='export_excel'),
]
