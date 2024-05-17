from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.permissions import IsAdmin
from dashboard.forms import CriterionCreationForm
from dashboard.models import KPI, Criterion
from users.models import User


class CriterionsView(IsAdmin, View):

    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:
        try:
            kpi = KPI.objects.get(id=kpi_id)
        except KPI.DoesNotExist:
            messages.info(request, "KPI maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect("dashboard:kpis")

        ctx = {
            "criterions": kpi.criterions.all(),
            "current_kpi": kpi,
            "kpis": KPI.objects.all(),
        }
        return render(request, 'dashboard/criterions/list.html', ctx)


class CriterionsCreateView(IsAdmin, View):

    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:
        try:
            kpi = KPI.objects.get(id=kpi_id)
        except KPI.DoesNotExist:
            messages.info(request, "KPI maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:criterions', kpi_id=kpi_id)

        ctx = {
            "current_kpi": kpi,
            "managers": User.objects.filter(role=User.MANAGER),
        }

        return render(request, 'dashboard/criterions/create.html', ctx)

    def post(self, request: HttpRequest, kpi_id: int) -> HttpResponse:
        create_form = CriterionCreationForm(request.POST)

        if create_form.is_valid():
            messages.success(request, "Yangi mezon muvaffaqiyatli yaratildi.")

            create_form.save()
            return redirect('dashboard:criterions', kpi_id=kpi_id)

        else:
            errors = create_form.errors

            for field, error_list in errors.items():
                for error in error_list:
                    messages.info(request, error)

            return redirect('dashboard:criterions', kpi_id=kpi_id)


class CriterionDetailView(IsAdmin, View):

    def get(self, request: HttpRequest, criterion_id: int) -> HttpResponse:
        try:
            criterion = Criterion.objects.get(id=criterion_id)
        except Criterion.DoesNotExist:
            messages.info(request, "Mezon maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')

        ctx = {
            "criterion": criterion,
        }

        return render(request, 'dashboard/criterions/detail.html', ctx)


class CriterionDeleteView(IsAdmin, View):
    
    def get(self, request: HttpRequest, criterion_id: int) -> HttpResponse:
        try:
            criterion = Criterion.objects.get(id=criterion_id)
        except Criterion.DoesNotExist:
            messages.info(request, "Mezon maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')
        
        criterion.delete()

        messages.success(request, "Mezon muvaffaqiyatli oʻchirildi.")
        return redirect('dashboard:criterions', kpi_id=criterion.kpi.id)


class CriterionUpdateView(IsAdmin, View):

    def get(self, request: HttpRequest, criterion_id: int) -> HttpResponse:
        try:
            criterion = Criterion.objects.get(id=criterion_id)
        except Criterion.DoesNotExist:
            messages.info(request, "Mezon maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')

        ctx = {
            "criterion": criterion,
            "managers": User.objects.filter(role=User.MANAGER),
        }

        return render(request, 'dashboard/criterions/update.html', ctx)
    
    def post(self, request: HttpRequest, criterion_id: int) -> HttpResponse:
        try:
            criterion = Criterion.objects.get(id=criterion_id)
        except Criterion.DoesNotExist:
            messages.info(request, "Mezon maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')

        update_form = CriterionCreationForm(request.POST, instance=criterion)

        if update_form.is_valid():
            update_form.save()

            messages.success(request, "Mezon muvaffaqiyatli tahrirlandi.")
            return redirect('dashboard:criterions', kpi_id=criterion.kpi.id)
        else:
            for field, error_list in errors.items():
                for error in error_list:
                    messages.info(request, error)

            return redirect('dashboard:criterions', kpi_id=criterion.kpi.id)
