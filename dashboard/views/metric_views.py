from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from users.permissions import IsManager, IsEmployee, IsManagerOrEmployee
from dashboard.forms import MetricCreationForm

from dashboard.models import KPI, Notefication, Metric
from users.models import User


class MetricsView(IsManagerOrEmployee, View):

    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:
        user: User = request.user

        try:
            kpi = KPI.objects.get(id=kpi_id)
        except KPI.DoesNotExist:
            messages.info(request, "KPI maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')

        ctx = {
            "kpi": kpi,
            "metrics": kpi.metrics.filter(parent=None),
        }
        if request.user.role == User.MANAGER:
            ctx['kpis'] = KPI.objects.filter(responsible_employee=request.user)
        else:
            ctx['kpis'] = KPI.objects.all()

        return render(request, 'dashboard/metrics/list.html', ctx)


class MetricCreateView(IsManager, View):

    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:
        user: User = request.user

        try:
            kpi = KPI.objects.get(id=kpi_id)
        except KPI.DoesNotExist:
            messages.info(request, "KPI maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')

        ctx = {
            "kpi": kpi,
            "kpis": KPI.objects.filter(responsible_employee=user),
            "metrics": kpi.metrics.all(),
        }

        return render(request, 'dashboard/metrics/create.html', ctx)

    def post(self, request: HttpRequest, kpi_id: int) -> HttpResponse:
        
        create_form = MetricCreationForm(request.POST)

        if create_form.is_valid():
            messages.success(request, "Yangi Metrik muvaffaqiyatli yaratildi.")

            create_form.save()
            return redirect('dashboard:main')

        else:
            messages.info(request, "Metrik maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")

            return redirect('dashboard:main')


class MetricDetailView(IsManagerOrEmployee, View):

    def get(self, request: HttpRequest, kpi_id: int, metric_id: int) -> HttpResponse:
        user = request.user

        try:
            kpi = KPI.objects.get(id=kpi_id)
            metric = kpi.metrics.get(id=metric_id)
        except KPI.DoesNotExist or Metric.DoesNotExist:
            messages.info(request, "Metrik maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')

        ctx = {
            "kpi": kpi,
            "metric": metric,
            "children": metric.children.all(),
        }
        if request.user.role == User.MANAGER:
            ctx['kpis'] = KPI.objects.filter(responsible_employee=request.user)
        else:
            ctx['kpis'] = KPI.objects.all()

        return render(request, 'dashboard/metrics/detail.html', ctx)


class MetricDeleteView(IsManager, View):

    def get(self, request: HttpRequest, kpi_id: int, metric_id: int) -> HttpResponse:
        user = request.user

        try:
            kpi = KPI.objects.get(id=kpi_id)
            metric = kpi.metrics.get(id=metric_id)
        except KPI.DoesNotExist or Metric.DoesNotExist:
            messages.info(request, "Metrik maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')
        metric.delete()

        messages.success(request, "Metrik muvaffaqiyatli oʻchirildi.")
        return redirect('dashboard:main')


class MetricUpdateView(IsManager, View):

    def get(self, request: HttpRequest, kpi_id: int, metric_id: int) -> HttpResponse:
        user = request.user

        try:
            kpi = KPI.objects.get(id=kpi_id)
            metric = kpi.metrics.get(id=metric_id)
        except KPI.DoesNotExist or Metric.DoesNotExist:
            messages.info(request, "Metrik maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')

        ctx = {
            "kpi": kpi,
            "deadline": metric.deadline.strftime('%Y-%m-%d'),
            "metric": metric,
            "metrics": kpi.metrics.all(),
            "kpis": KPI.objects.filter(responsible_employee=user),
        }

        return render(request, 'dashboard/metrics/update.html', ctx)
    
    def post(self, request: HttpRequest, kpi_id: int, metric_id: int) -> HttpResponse:
        user = request.user

        try:
            kpi = KPI.objects.get(id=kpi_id)
            metric = kpi.metrics.get(id=metric_id)
        except KPI.DoesNotExist or Metric.DoesNotExist:
            messages.info(request, "Metrik maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')

        update_form = MetricCreationForm(request.POST, instance=metric)

        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Metrik muvaffaqiyatli tahrirlandi.")
            return redirect('dashboard:main')
        else:
            messages.info(request, "Metrik maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')


class MetricsAPIView(IsEmployee, View):

    def get(self, request: HttpRequest) -> JsonResponse:
        try:
            kpi_id = request.GET.get("kpi_id")
            kpi = KPI.objects.get(id=kpi_id)
        except KPI.DoesNotExist:
            messages.info(request, "KPI maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")

            return JsonResponse([], safe=False)
        
        data = []
        for metric in kpi.metrics.all():
            data.append({
                "id": metric.id,
                "name": metric.name
            })
        
        return JsonResponse(data, safe=False)
