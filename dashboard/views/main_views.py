from datetime import date
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.models import User, Department
from dashboard.models import KPI


class DashboardView(LoginRequiredMixin, View):
    
    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user

        if user.role == User.ADMIN:
            ctx = {
                "kpis": KPI.objects.all(),
                "departments": Department.objects.all(),
                "employees": User.objects.filter(role=User.EMPLOYEE),
            }

            return render(request, "dashboard/main/admin.html", ctx)
