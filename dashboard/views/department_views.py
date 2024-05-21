from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.permissions import IsACM
from users.models import User, Department


class DepartmentView(IsACM, View):

    def get(self, request: HttpRequest) -> HttpResponse:

        ctx = {
            "departments": Department.objects.all(),
        }

        return render(request, 'dashboard/departments/list.html', ctx)
