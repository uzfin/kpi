from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from dashboard.models import KPI
from users.permissions import IsACM
from users.models import User


class EmployeesView(IsACM, View):

    def get(self, request: HttpRequest) -> HttpResponse:
        current_kpi = request.session['current_kpi']
        try:
            current_kpi = KPI.objects.get(id=current_kpi['id'])
        except (KPI.DoesNotExist, ValueError) as e:
            current_kpi = KPI.objects.last()
            messages.info(request, "KPI ma'lumotlari bilan xatolik yuz berdi. Iltimos yana bir bor urinib ko'ring.")

        employees = []
        ems = User.objects.filter(role=User.EMPLOYEE)
        for employee in ems:
            data = {
                "id": employee.id,
                "name": employee.full_name,
                "profile_picture": employee.profile_picture.url,
                "departments": ', '.join([department.name for department in employee.working_departments.all()])
            }
            try:
                result = employee.results.get(kpi=current_kpi)
                data["ball"] = result.ball
                data["percent"] = round(result.ball / current_kpi.ball * 100)
                employees.append(data)
            except:
                data["ball"] = 0
                data["percent"] = 0
                employees.append(data)              
            
        employees = sorted(employees, key=lambda em: em['ball'], reverse=True)
        ctx = {
            'employees': employees,
            'count': ems.count()
        }

        return render(request, 'dashboard/employees/list.html', ctx)
