from datetime import date, datetime, timedelta
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models import Count, functions as db_functions

from users.permissions import IsACM
from users.models import User, Department
from dashboard.models import KPI, Submission, Result, Clause


class ReporterView(IsACM, View):
    
    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:
        try:
            kpi = KPI.objects.get(id=kpi_id)

            if 'current_kpi' in request.session:
                del request.session['current_kpi']
            request.session['current_kpi'] = {"id": kpi.id, "name": kpi.name}
        except KPI.DoesNotExist:
            messages.info(request, "KPI ma'lumotlarida xatolik yuz berdi.")
            return redirect("dashboard:main")
        
        monthly_submissions = kpi.submissions.annotate(
            year=db_functions.ExtractYear('created_at'),
            month=db_functions.ExtractMonth('created_at')
        ).values('year', 'month').annotate(count=Count('id')).order_by('year', 'month')
        
        departments_data = []
        for department in Department.objects.all():
            department_data = {
                "name": department.name,
                "submmission_count": 0
            }
            for employee in department.employees.all():
                department_data['submmission_count'] += employee.submissions.filter(kpi=kpi).count()
            
            departments_data.append(department_data)
        
        ctx = {
            "kpis": KPI.objects.all(),
            "kpis_data": monthly_submissions,
            "departments_data": departments_data,
        }
        return render(request, "dashboard/reporters/main.html", ctx)


class ReporterKPIView(IsACM, View):
    
    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:
        try:
            kpi = KPI.objects.get(id=kpi_id)

            if 'current_kpi' in request.session:
                del request.session['current_kpi']
            request.session['current_kpi'] = {"id": kpi.id, "name": kpi.name}
        except KPI.DoesNotExist:
            messages.info(request, "KPI ma'lumotlarida xatolik yuz berdi.")
            return redirect("dashboard:main")
        
        employees_data = []
        for employee in User.objects.filter(role=User.EMPLOYEE):
            employee_data = {
                "employee": employee,
                "count": employee.submissions.filter(kpi=kpi).count(),
                "departments": ", ".join([department.name for department in employee.working_departments.all()]),
            }
            employees_data.append(employee_data)
        
        clauses_without_children = Clause.objects.annotate(num_children=Count('children')).filter(num_children=0)
        
        ctx = {
            "kpis": KPI.objects.all(),
            "clauses": clauses_without_children.count(),
            "employees_data": sorted(employees_data, key=lambda employee: employee['count'], reverse=True),
        }
        print(clauses_without_children.count())
        return render(request, "dashboard/reporters/kpi.html", ctx)
