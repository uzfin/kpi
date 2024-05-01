from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.permissions import IsCEO, IsCeoOrEmployee
from dashboard.forms import KPICreationForm

from dashboard.models import KPI, Notefication
from users.models import User


class KPIView(IsCeoOrEmployee, View):

    def get(self, request: HttpRequest) -> HttpResponse:

        ctx = {
            "kpis": KPI.objects.all(),
        }

        return render(request, 'dashboard/kpis/list.html', ctx)


class KPICreateView(IsCEO, View):

    def get(self, request: HttpRequest) -> HttpResponse:

        ctx = {
            "managers": User.objects.filter(role=User.MANAGER),
        }

        return render(request, 'dashboard/kpis/create.html', ctx)

    def post(self, request: HttpRequest) -> HttpResponse:
        
        create_form = KPICreationForm(request.POST)

        if create_form.is_valid():
            messages.success(request, "Yangi KPI muvaffaqiyatli yaratildi.")

            create_form.save()
            return redirect('dashboard:kpi')

        else:
            messages.info(request, "KPI maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")

            return redirect('dashboard:create-kpi')


class KPIDetailView(IsCeoOrEmployee, View):

    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:

        try:
            kpi = KPI.objects.get(id=kpi_id)
        except KPI.DoesNotExist:
            messages.info(request, "KPI maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:kpi')

        ctx = {
            "kpi": kpi,
        }

        return render(request, 'dashboard/kpis/detail.html', ctx)


class KPIDeleteView(IsCEO, View):

    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:

        try:
            kpi = KPI.objects.get(id=kpi_id)
            kpi.delete()
        except KPI.DoesNotExist:
            messages.info(request, "KPI maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:kpi')

        messages.success(request, "KPI muvaffaqiyatli oʻchirildi.")
        return redirect('dashboard:kpi')


class KPIUpdateView(IsCEO, View):

    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:

        try:
            kpi = KPI.objects.get(id=kpi_id)
        except KPI.DoesNotExist:
            messages.info(request, "KPI maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:kpi')

        ctx = {
            "kpi": kpi,
            "managers": User.objects.filter(role=User.MANAGER),
        }

        return render(request, 'dashboard/kpis/update.html', ctx)
    
    def post(self, request: HttpRequest, kpi_id: int) -> HttpResponse:

        try:
            kpi = KPI.objects.get(id=kpi_id)
        except KPI.DoesNotExist:
            messages.info(request, "KPI maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:kpi')

        update_form = KPICreationForm(request.POST, instance=kpi)

        if update_form.is_valid():
            update_form.save()
            messages.success(request, "KPI muvaffaqiyatli tahrirlandi.")
            return redirect('dashboard:kpi')
        else:
            messages.info(request, "KPI maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:kpi')
