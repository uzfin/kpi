from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpRequest, HttpResponse
from .models import KPI

from users.models import User


class DashboardView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest) -> HttpResponse:
        user: User = request.user

        ctx = {
            "user": user,
            "root_user": User,
            "kpis": KPI.objects.all(),
        }

        return render(request, 'dashboard/main.html', ctx)

        # pairs = []
        # for i in range(0, len(kpis), 2):
        #     if i + 1 < len(kpis):
        #         pairs.append((kpis[i], kpis[i + 1]))
        #     else:
        #         pairs.append((kpis[i],))
                    
        # return render(request, "dashboard/ceo.html", {"user": request.user, "kpis": pairs})
