from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from dashboard.forms import DepartmentCreationForm
from users.permissions import IsACM, IsAdmin
from users.models import User, Department


class DepartmentView(IsACM, View):

    def get(self, request: HttpRequest) -> HttpResponse:

        ctx = {
            "departments": Department.objects.all(),
        }

        return render(request, 'dashboard/departments/list.html', ctx)


class DepartmentCreateView(IsAdmin, View):

    def get(self, request: HttpRequest) -> HttpResponse:

        ctx = {
            "employees": User.objects.all(),
        }

        return render(request, 'dashboard/departments/create.html', ctx)

    def post(self, request: HttpRequest) -> HttpResponse:
        create_form = DepartmentCreationForm(request.POST)

        if create_form.is_valid():
            messages.success(request, "Yangi bo'lim muvaffaqiyatli yaratildi.")

            create_form.save()
            return redirect('dashboard:departments')

        else:
            errors = create_form.errors

            for field, error_list in errors.items():
                for error in error_list:
                    messages.info(request, error)

            return redirect('dashboard:departments')


class DepartmentDetailView(IsACM, View):

    def get(self, request: HttpRequest, department_id: int) -> HttpResponse:
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            messages.info(request, "Bo'lim ma'lumotlarida xatolik yuz berdi.")
            return redirect("dashboard:departments")

        ctx = {
            "department": department,
        }

        return render(request, 'dashboard/departments/detail.html', ctx)


class DepartmentDeleteView(IsAdmin, View):

    def get(self, request: HttpRequest, department_id: int) -> HttpResponse:
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            messages.info(request, "Bo'lim ma'lumotlarida xatolik yuz berdi.")
            return redirect("dashboard:departments")

        department.delete()
        messages.success(request, "Bo'lim muvaffaqiyatli o'chirildi.")
        
        return redirect("dashboard:departments")


class DepartmentUpdateView(IsAdmin, View):

    def get(self, request: HttpRequest, department_id: int) -> HttpResponse:
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            messages.info(request, "Bo'lim ma'lumotlarida xatolik yuz berdi.")
            return redirect("dashboard:departments")

        ctx = {
            "department": department,
            "employees": User.objects.all(),
        }
        
        return render(request, 'dashboard/departments/update.html', ctx)

    def post(self, request: HttpRequest, department_id: int) -> HttpResponse:
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            messages.info(request, "Bo'lim ma'lumotlarida xatolik yuz berdi.")
            return redirect("dashboard:departments")

        update_form = DepartmentCreationForm(request.POST, instance=department)

        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Bo'lim muvaffaqiyatli tahrirlandi.")
            return redirect('dashboard:department-detail', department_id=department_id)
        else:
            errors = update_form.errors

            for field, error_list in errors.items():
                for error in error_list:
                    messages.info(request, error)
            return redirect('dashboard:department-detail', department_id=department_id)
