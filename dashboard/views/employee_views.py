from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.permissions import IsAdmin
from users.models import User


class EmployeesView(IsAdmin, View):

    def get(self, request: HttpRequest) -> HttpResponse:
        ctx = {
            "employees": User.objects.filter(role__in=(User.GUEST, User.EMPLOYEE, User.BOSS, User.MANAGER, User.CEO)),
        }

        return render(request, 'dashboard/employees/list.html', ctx)
