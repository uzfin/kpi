from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpRequest, HttpResponse
from .models import KPI, Notefication

from users.models import User


class DashboardView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest) -> HttpResponse:
        user: User = request.user
        kpis = KPI.objects.all()

        today = date.today()

        pairs = []
        for i in range(0, len(kpis), 2):
            if i + 1 < len(kpis):
                data1 = {
                    "id": kpis[i].id,
                    "name": kpis[i].name,
                    "total": kpis[i].total_ball,
                    "ball": 0,
                    "date": today
                }
                for submission in user.submissions.filter(metric__kpi=kpis[i]):
                    data1['ball'] += submission.ball

                data1['percent'] = round(data1['ball'] / data1['total'], 2) * 100

                data2 = {
                    "id": kpis[i + 1].id,
                    "name": kpis[i + 1].name,
                    "total": kpis[i + 1].total_ball,
                    "ball": 0,
                    "date": today
                }
                for submission in user.submissions.filter(metric__kpi=kpis[i + 1]):
                    data2['ball'] += submission.ball

                data2['percent'] = round(data2['ball'] / data2['total'], 2) * 100

                pairs.append((data1,data2))
            else:
                data = {
                    "id": kpis[i].id,
                    "name": kpis[i].name,
                    "total": kpis[i].total_ball,
                    "ball": 0,
                    "date": today
                }
                for submission in user.submissions.filter(metric__kpi=kpis[i]):
                    data['ball'] += submission.ball

                data['percent'] = round(data['ball'] / data['total'], 2) * 100

                pairs.append((data,))

        ctx = {
            "user": user,
            "root_user": User,
            "kpis": kpis,
            "pairs": pairs,
            "notefications": user.notefications.filter(unread=True).all()
        }

        return render(request, 'dashboard/main.html', ctx)
                    
        # return render(request, "dashboard/ceo.html", {"user": request.user, "kpis": pairs})
