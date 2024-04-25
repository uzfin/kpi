from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from users.permissions import IsCEO
from django.views import View
from django.http import HttpRequest, HttpResponse
from .forms import KPICreationForm

from .models import KPI, Notefication, Department
from users.models import User


class DashboardView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest) -> HttpResponse:
        user: User = request.user
        kpis = KPI.objects.all()

        pairs = []
        if user.role == User.EMPLOYEE:
            for i in range(0, len(kpis), 2):
                if len(pairs) == 2: break

                if i + 1 < len(kpis):
                    pairs.append((user.get_kpi_status(kpis[i]), user.get_kpi_status(kpis[i + 1])))
                else:
                    pairs.append((user.get_kpi_status(kpis[i]),))
        else:
            users = User.objects.filter(role=User.EMPLOYEE)
            n = len(users)
            
            for i in range(0, len(kpis), 2):
                if len(pairs) == 2: break

                if i + 1 < len(kpis):
                    percent1, percent2 = 0, 0
                    ball1, ball2 = 0, 0
                    
                    for user in users:
                        data1 = user.get_kpi_status(kpis[i])
                        percent1 += data1['percent']
                        ball1 += data1['ball']

                        data2 = user.get_kpi_status(kpis[i + 1])
                        percent2 += data2['percent']
                        ball2 += data2['ball']

                    pairs.append(
                        (
                            {
                                "id": kpis[i].id,
                                "name": kpis[i].name,
                                "percent": percent1,
                                "total": kpis[i].total_ball,
                                "ball": round(ball1 / n)
                            },
                            {
                                "id": kpis[i + 1].id,
                                "name": kpis[i + 1].name,
                                "percent": percent2,
                                "total": kpis[i + 1].total_ball,
                                "ball": round(ball2 / n)
                            }
                        )
                    )
                else:
                    percent = 0
                    ball = 0
                    
                    for user in users:
                        data = user.get_kpi_status(kpis[i])
                        percent += data1['percent']
                        ball += data1['ball']

                    pairs.append(
                        (
                            {
                                "id": kpis[i].id,
                                "name": kpis[i].name,
                                "percent": percent,
                                "total": kpis[i].total_ball,
                                "ball": round(ball / n)
                            },
                        )
                    )

            # TODO: status of departments

        ctx = {
            "user": request.user,
            "root_user": User,
            "kpis": kpis,
            "pairs": pairs,
            "notefications": user.notefications.filter(unread=True).all(),
            "date": date.today()
        }

        return render(request, 'dashboard/main.html', ctx)


class KPIView(IsCEO, View):

    def get(self, request: HttpRequest) -> HttpResponse:

        ctx = {
            "user": request.user,
            "root_user": User,
            "kpis": KPI.objects.all(),
            "notefications": request.user.notefications.filter(unread=True).all(),
            "date": date.today()
        }

        return render(request, 'dashboard/kpis/list.html', ctx)


class KPICreateView(IsCEO, View):

    def get(self, request: HttpRequest) -> HttpResponse:

        ctx = {
            "user": request.user,
            "root_user": User,
            "managers": User.objects.filter(role=User.MANAGER),
            "notefications": request.user.notefications.filter(unread=True).all(),
        }

        return render(request, 'dashboard/kpis/create.html', ctx)

    def post(self, request: HttpRequest) -> HttpResponse:
        
        create_form = KPICreationForm(request.POST)

        if create_form.is_valid():
            messages.success(request, "New KPI has been created succesfully.")

            create_form.save()
            return redirect('dashboard:kpi')

        else:
            messages.info(request, "There was an error with kpi data. Please try again.")

            return redirect('dashboard:create-kpi')


class KPIDetailView(IsCEO, View):

    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:

        try:
            kpi = KPI.objects.get(id=kpi_id)
        except KPI.DoesNotExist:
            messages.info(request, "There was an error with kpi data. Please try again.")
            return redirect('dashboard:kpi')

        ctx = {
            "user": request.user,
            "root_user": User,
            "kpi": kpi,
            "notefications": request.user.notefications.filter(unread=True).all(),
        }

        return render(request, 'dashboard/kpis/detail.html', ctx)

    def post(self, request: HttpRequest) -> HttpResponse:
        
        create_form = KPICreationForm(request.POST)

        if create_form.is_valid():
            messages.success(request, "New KPI has been created succesfully.")

            create_form.save()
            return redirect('dashboard:kpi')

        else:
            messages.info(request, "There was an error with kpi data. Please try again.")

            return redirect('dashboard:create-kpi')


class KPIDeleteView(IsCEO, View):

    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:

        try:
            kpi = KPI.objects.get(id=kpi_id)
            kpi.delete()
        except KPI.DoesNotExist:
            messages.info(request, "There was an error with kpi data. Please try again.")
            return redirect('dashboard:kpi')

        messages.success(request, "KPI has been deleted succesfully.")
        return redirect('dashboard:kpi')


class KPIUpdateView(IsCEO, View):

    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:

        try:
            kpi = KPI.objects.get(id=kpi_id)
        except KPI.DoesNotExist:
            messages.info(request, "There was an error with kpi data. Please try again.")
            return redirect('dashboard:kpi')

        ctx = {
            "user": request.user,
            "root_user": User,
            "kpi": kpi,
            "managers": User.objects.filter(role=User.MANAGER),
            "notefications": request.user.notefications.filter(unread=True).all(),
        }

        return render(request, 'dashboard/kpis/update.html', ctx)
    
    def post(self, request: HttpRequest, kpi_id: int) -> HttpResponse:

        try:
            kpi = KPI.objects.get(id=kpi_id)
        except KPI.DoesNotExist:
            messages.info(request, "There was an error with kpi data. Please try again.")
            return redirect('dashboard:kpi')

        update_form = KPICreationForm(request.POST, instance=kpi)

        if update_form.is_valid():
            update_form.save()
            messages.success(request, "KPI has been updated succesfully.")
            return redirect('dashboard:kpi')
        else:
            messages.info(request, "There was an error with kpi data. Please try again.")
            return redirect('dashboard:kpi')
