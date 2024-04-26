from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpRequest, HttpResponse

from dashboard.models import KPI, Notefication
from users.models import User


class DashboardView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest) -> HttpResponse:
        user: User = request.user

        if user.role == User.MANAGER:
            kpis = KPI.objects.filter(responsible_employee=user)
        else:
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
                        percent += data['percent']
                        ball += data['ball']

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

