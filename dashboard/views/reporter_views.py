from datetime import date, datetime, timedelta
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from users.permissions import IsACM
from users.models import User, Department
from dashboard.models import KPI, Submission, Result


def get_monthly_report(kpi):
    today = date.today()
    if kpi.end_date > today:
        start_date, end_date = kpi.start_date, today
    else:
        start_date, end_date = kpi.start_date, kpi.end_date

    results = kpi.submissions

    # Generate a list of months between start_date and end_date
    monthly_report = []
    current_date = start_date.replace(day=1)

    while current_date <= end_date:
        month_str = current_date.strftime("%m-%Y")
        total_ball = results.filter()
        monthly_report.append({
            "month": month_str, 
            "ball": total_ball
        })
        # Move to the next month
        next_month = current_date + timedelta(days=32)
        current_date = next_month.replace(day=1)

    return monthly_report


class ReporterView(IsACM, View):
    
    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:
        try:
            kpi = KPI.objects.get(id=kpi_id)
        except KPI.DoesNotExist:
            messages.info(request, "KPI ma'lumotlarida xatolik yuz berdi.")
            return redirect("dashboard:main")
        
        kpis_data = get_monthly_report(kpi)

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
            "kpis_data": general_data,
            "department_data": departments_data,
        }
        return render(request, "dashboard/reporters/main.html", ctx)
