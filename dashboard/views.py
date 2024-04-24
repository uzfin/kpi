from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpRequest, HttpResponse
from .models import KPI, Notefication, Department
from users.models import User


class DashboardView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest) -> HttpResponse:
        user: User = request.user
        kpis = KPI.objects.all()

        pairs = []
        for i in range(0, len(kpis), 2):
            if i + 1 < len(kpis):
                pairs.append((user.get_kpi_status(kpis[i]), user.get_kpi_status(kpis[i + 1])))
            else:
                pairs.append((user.get_kpi_status(kpis[i]),))

        ctx = {
            "user": user,
            "root_user": User,
            "kpis": kpis,
            "pairs": pairs,
            "notefications": user.notefications.filter(unread=True).all(),
            "date": date.today()
        }

        return render(request, 'dashboard/main.html', ctx)
                    
        # return render(request, "dashboard/ceo.html", {"user": request.user, "kpis": pairs})
