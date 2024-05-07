from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.permissions import IsCeoOrManager

from dashboard.models import Department, KPI
from users.models import User


class DepartmentView(IsCeoOrManager, View):

    def get(self, request: HttpRequest) -> HttpResponse:

        ctx = {
            "departments": Department.objects.all(),
        }
        if request.user.role == User.MANAGER:
            ctx['kpis'] = KPI.objects.filter(responsible_employee=request.user)

        return render(request, 'dashboard/departments/list.html', ctx)
