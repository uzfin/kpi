from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.permissions import IsManager, IsACM
from dashboard.models import Submission, KPI
from dashboard.forms import MarkForm
from users.models import User


class WorksView(IsACM, View):

    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:
        try:
            current_kpi = KPI.objects.get(id=kpi_id)
        except KPI.DoesNotExist:
            messages.info(request, "KPI ma'lumotlarida xatolik yuz berdi.")
            return redirect("dashboard:main")

        if request.user.role == User.MANAGER:
            works = current_kpi.submissions.filter(clause__criterion__in=request.user.criterions.all()).order_by('-updated_at')
        elif request.user.role == User.CEO:
            works = current_kpi.submissions.order_by('-updated_at')
        ctx = {
            'works': works
        }
        return render(request, 'dashboard/works/list.html', ctx)


class WorkDetailView(IsACM, View):

    def get(self, request: HttpRequest, work_id: int) -> HttpResponse:
        
        try:
            submission = Submission.objects.get(id=work_id)
            if request.user.role == User.MANAGER:
                submission.is_checked = True
                submission.save()

        except Submission.DoesNotExist:
            messages.info(request, "Hisobot maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")

        ctx = {
            'work': submission
        }
        return render(request, 'dashboard/works/detail.html', ctx)


class AssessmentView(IsManager, View):

    def post(self, request: HttpRequest, work_id: int) -> HttpResponse:
        
        try:
            submission = Submission.objects.get(id=work_id)

        except Submission.DoesNotExist:
            messages.info(request, "Hisobot maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect("dashboard:main")

        update_form = MarkForm(request.POST, instance=submission.mark)
        if update_form.is_valid():
            update_form.save()
            submission.is_marked = True
            submission.save()

            messages.success(request, "Hisobotni muvaffaqiyatli baholadingiz.")
            return redirect("dashboard:work-detail", work_id=work_id)

        errors = create_form.errors
        for field, error_list in errors.items():
            for error in error_list:
                messages.info(request, error)

        return redirect("dashboard:work-detail", work_id=work_id)
