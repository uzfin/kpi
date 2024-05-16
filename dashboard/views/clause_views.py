from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.permissions import IsAdmin
from dashboard.forms import ClauseCreationForm
from dashboard.models import KPI, Criterion
from users.models import User


class ClauseCreateView(IsAdmin, View):

    def get(self, request: HttpRequest, criterion_id: int) -> HttpResponse:
        try:
            criterion = Criterion.objects.get(id=criterion_id)
        except Criterion.DoesNotExist:
            messages.info(request, "Mezon maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:criterion')

        ctx = {
            "criterion": criterion,
        }

        return render(request, 'dashboard/clauses/create.html', ctx)

    def post(self, request: HttpRequest, criterion_id: int) -> HttpResponse:
        create_form = ClauseCreationForm(request.POST)

        if create_form.is_valid():
            messages.success(request, "Yangi band muvaffaqiyatli yaratildi.")

            create_form.save()
            return redirect('dashboard:criterion-detail', criterion_id=criterion_id)

        else:
            errors = create_form.errors

            for field, error_list in errors.items():
                for error in error_list:
                    messages.info(request, error)

            return redirect('dashboard:criterion-detail', criterion_id=criterion_id)

