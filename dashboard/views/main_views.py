from datetime import date
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.models import User, Department
from dashboard.models import KPI, Criterion, Result


class DashboardView(LoginRequiredMixin, View):
    
    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user

        # get kpi_id to indentify getting data from which KPI
        kpi_id = request.GET.get("kpi_id")

        # check kpi_id
        if kpi_id:
            try:
                kpi_id_int = int(kpi_id)
                current_kpi = KPI.objects.get(id=kpi_id_int)
            except (KPI.DoesNotExist, ValueError) as e:
                current_kpi = KPI.objects.last()
                messages.info(request, "KPI ma'lumotlari bilan xatolik yuz berdi. Iltimos yana bir bor urinib ko'ring.")
        else:
            current_kpi = KPI.objects.last()

        if current_kpi:
            if 'current_kpi' in request.session:
                del request.session['current_kpi']
            request.session['current_kpi'] = {'id': current_kpi.id, 'name': current_kpi.name, 'ball': current_kpi.ball}

        if user.role == User.ADMIN or user.role == User.CEO:
            ctx = {
                "kpis": KPI.objects.all(),
                "departments": Department.objects.all()[:10],
            }
            employees = []
            for employee in User.objects.filter(role=User.EMPLOYEE):
                data = {
                    "id": employee.id,
                    "name": employee.full_name,
                    "profile_picture": employee.profile_picture.url
                }
                try:
                    result = employee.results.get(kpi=current_kpi)
                    data["ball"] = result.ball
                    data["percent"] = round(result.ball / current_kpi.ball * 100)
                    employees.append(data)
                except:
                    pass               
                
            employees = sorted(employees, key=lambda em: em['ball'], reverse=True)
            ctx['employees'] = employees

            return render(request, "dashboard/main/admin.html", ctx)

        elif user.role == User.MANAGER:
            ctx = {
                "departments": Department.objects.all()[:10],
                "employees": User.objects.filter(role=User.EMPLOYEE)[:10],
            }
            if current_kpi:
                ctx['criterions'] = Criterion.objects.filter(kpi=current_kpi, responsible_person=user)
            return render(request, "dashboard/main/manager.html", ctx)

        elif user.role == User.BOSS:
            department = user.departments.first()
            employees = []
            for employee in department.employees.all():
                data = {
                    "id": employee.id,
                    "name": employee.full_name,
                    "profile_picture": employee.profile_picture.url
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
                "department": department,
                "employees": employees,
            }
            return render(request, "dashboard/main/boss.html", ctx)
        
        elif user.role == User.EMPLOYEE:
            try:
                ball = Result.objects.get(employee=user, kpi=current_kpi).ball
                done = round(ball / current_kpi.ball * 100)
            except Result.DoesNotExist:
                ball = 0
                done = 0

            working_departments = user.working_departments.first()
            colleagues = []
            for colleague in working_departments.employees.all():
                data = {
                    "id": colleague.id,
                    "name": colleague.full_name,
                    "profile_picture": colleague.profile_picture.url,
                }
                try:
                    ball = Result.objects.get(employee=colleague, kpi=current_kpi).ball
                    done = round(ball / current_kpi.ball * 100)
                    data['ball'] = ball
                    data['percent'] = done
                    colleagues.append(data)
                except Result.DoesNotExist:
                    ball = 0
                    done = 0
                    data['ball'] = ball
                    data['percent'] = done
                    colleagues.append(data)
            colleagues = sorted(colleagues, key=lambda c: c['ball'], reverse=True)
            ctx = {
                "colleagues": colleagues,
                "ball": ball,
                "done": done,
                "undone": 100 - done,
                "kpis": KPI.objects.all(),
            }
            return render(request, "dashboard/main/employee.html", ctx)

        elif user.role == User.GUEST:
            ctx = {

            }
            return render(request, "dashboard/main/guest.html", ctx)

        else:
            pass
