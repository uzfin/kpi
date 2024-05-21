from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.permissions import IsACM
from users.models import User, Department


class EmployeeView(IsACM, View):

    def get(self, request: HttpRequest, department_id: int) -> HttpResponse:

        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist: 
            messages.info(request, "Department maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:departments')

        ctx = {
            "employees": department.employees.all(),
        }

        return render(request, 'dashboard/employees/list.html', ctx)
