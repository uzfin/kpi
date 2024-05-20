from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.permissions import IsAdmin
from dashboard.forms import ClauseCreationForm
from dashboard.models import Clause, Criterion
from users.models import User


class ClauseDetailView(IsAdmin, View):

    def get(self, request: HttpRequest, clause_id: int) -> HttpResponse:
        try:
            clause = Clause.objects.get(id=clause_id)
        except Clause.DoesNotExist:
            messages.info(request, "Band maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:criterion')

        ctx = {
            "clause": clause,
        }

        return render(request, 'dashboard/clauses/detail.html', ctx)


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


class ClauseInternalCreateView(IsAdmin, View):

    def get(self, request: HttpRequest, parent_clause_id: int) -> HttpResponse:
        try:
            parent_clause = Clause.objects.get(id=parent_clause_id)
        except Clause.DoesNotExist:
            messages.info(request, "Band maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')

        ctx = {
            "parent_clause": parent_clause,
        }

        return render(request, 'dashboard/clauses/internal-create.html', ctx)

    def post(self, request: HttpRequest, parent_clause_id: int) -> HttpResponse:
        create_form = ClauseCreationForm(request.POST)

        if create_form.is_valid():
            messages.success(request, "Yangi band muvaffaqiyatli yaratildi.")

            create_form.save()
            return redirect('dashboard:clause-detail', clause_id=parent_clause_id)

        else:
            errors = create_form.errors

            for field, error_list in errors.items():
                for error in error_list:
                    messages.info(request, error)

            return redirect('dashboard:clause-detail', clause_id=parent_clause_id)


class ClauseDeleteView(IsAdmin, View):

    def get(self, request: HttpRequest, clause_id: int) -> HttpResponse:
        try:
            clause = Clause.objects.get(id=clause_id)
        except Clause.DoesNotExist:
            messages.info(request, "Band maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')

        clause.delete()
        messages.success(request, "Band muvaffaqiyatli o'chirildi.")

        return redirect("dashboard:criterion-detail", criterion_id=clause.criterion.id)

