from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.permissions import IsEmployee
from dashboard.forms import SubmissionCreationForm

from dashboard.models import KPI, Notefication
from users.models import User


class SubmissionsView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user

        if user.role == User.EMPLOYEE:
            submissions = user.submissions.order_by("-submitted_at")
        elif user.role == User.MANAGER:
            submissions = user.submissions.filter(metric__kpi__in=KPI.objects.filter(responsible_employee=user)).order_by("-submitted_at")

        ctx = {
            "submissions": submissions
        }

        return render(request, 'dashboard/submissions/list.html', ctx)


class SubmissionCreateView(IsEmployee, View):

    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user

        ctx = {
            "kpis": KPI.objects.all(),
        }

        return render(request, 'dashboard/submissions/create.html', ctx)

    def post(self, request: HttpRequest) -> HttpResponse:
        user = request.user

        create_form = SubmissionCreationForm(request.POST, request.FILES)

        if create_form.is_valid():
            instance = create_form.instance

            instance.save()

            messages.success(request, "Ishingiz muvaffaqiyatli joylandi.")
            return redirect('dashboard:submissions')

        else:
            print(create_form.errors)
            messages.info(request, "Ishingizni joylashda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:submissions')