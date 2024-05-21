from datetime import date
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.models import User, Department
from dashboard.models import KPI, Criterion


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
            request.session['current_kpi'] = {'id': current_kpi.id, 'name': current_kpi.name}

        if user.role == User.ADMIN or user.role == User.CEO:
            ctx = {
                "kpis": KPI.objects.all(),
                "departments": Department.objects.all()[:10],
                "employees": User.objects.filter(role=User.EMPLOYEE)[:10],
            }
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
            ctx = {

            }
            return render(request, "dashboard/main/boss.html", ctx)
        
        elif user.role == User.EMPLOYEE:
            ctx = {
                "colleagues": User.objects.all()
            }
            return render(request, "dashboard/main/employee.html", ctx)

        elif user.role == User.GUEST:
            ctx = {

            }
            return render(request, "dashboard/main/guest.html", ctx)

        else:
            pass
