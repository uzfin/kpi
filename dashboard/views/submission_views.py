from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.permissions import IsEmployee, IsManager
from dashboard.forms import SubmissionCreationForm
from dashboard.models import KPI, Notefication, Submission
from users.models import User


class SubmissionsView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user

        if user.role == User.EMPLOYEE:
            submissions = user.submissions.order_by("-submitted_at")
        elif user.role == User.MANAGER:
            submissions = Submission.objects.filter(metric__kpi__in=KPI.objects.filter(responsible_employee=user), is_checked=False).order_by("-submitted_at")

        ctx = {
            "submissions": submissions
        }
        if request.user.role == User.MANAGER:
            ctx['kpis'] = KPI.objects.filter(responsible_employee=request.user)

        return render(request, 'dashboard/submissions/list.html', ctx)


class SubmissionCreateView(IsEmployee, View):

    def get(self, request: HttpRequest, kpi_id: int, metric_id: int) -> HttpResponse:

        try:
            kpi = KPI.objects.get(id=kpi_id)
            metric = kpi.metrics.get(id=metric_id)
        except KPI.DoesNotExist or Metric.DoesNotExist:
            messages.info(request, "Metrik maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')

        user = request.user

        ctx = {
            "kpi": kpi,
            "metric": metric,
        }

        return render(request, 'dashboard/submissions/create.html', ctx)

    def post(self, request: HttpRequest, kpi_id: int, metric_id: int) -> HttpResponse:
        user = request.user

        create_form = SubmissionCreationForm(request.POST, request.FILES)

        if create_form.is_valid():
            instance = create_form.instance

            instance.save()

            messages.success(request, "Ishingiz muvaffaqiyatli joylandi.")
            return redirect('dashboard:submissions')

        else:
            messages.info(request, "Ishingizni joylashda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring. Oldin joylagan bo'lishingiz mumkin.")
            return redirect('dashboard:submissions')


# class SubmissionDetailView(IsEmployee, View):

#     def get(self, request: HttpRequest, submission_id: int) -> HttpResponse:

#         try:
#             submission = request.user.submissions.get(id=submission_id)
#         except Submission.DoesNotExist:
#             messages.info(request, "Hisobot maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
#             return redirect('dashboard:submissions')

#         ctx = {
#             "submission": submission,
#         }

#         return render(request, 'dashboard/submissions/detail.html', ctx)


# class SubmissionUpdateView(IsEmployee, View):

#     def get(self, request: HttpRequest, submission_id: int) -> HttpResponse:

#         try:
#             submission = request.user.submissions.get(id=submission_id)
#         except Submission.DoesNotExist:
#             messages.info(request, "Hisobot maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
#             return redirect('dashboard:submissions')

#         ctx = {
#             "submission": submission,
#         }

#         return render(request, 'dashboard/submissions/update.html', ctx)

#     def post(self, request: HttpRequest, submission_id: int) -> HttpResponse:

#         try:
#             submission = request.user.submissions.get(id=submission_id)
#         except Submission.DoesNotExist:
#             messages.info(request, "Hisobot maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
#             return redirect('dashboard:submissions')

#         update_form = SubmissionUpdationForm(request.POST, request.FILES, instance=submission)
#         if update_form.is_valid():
#             update_form.save()

#             messages.success(request, "Hisobotingiz muvaffaqiyatli yangilandi.")
#             return redirect("dashboard:submissions")

#         ctx = {
#             "submission": submission,
#         }
#         messages.info(request, "Hisobotingizni yangilashda xatolik yuz berdi. Iltimos, yana bir bor uninib ko'ring.")
#         return render(request, 'dashboard/submissions/update.html', ctx)


# class SubmissionDeleteView(IsEmployee, View):

#     def get(self, request: HttpRequest, submission_id: int) -> HttpResponse:

#         try:
#             submission = request.user.submissions.get(id=submission_id)
#             submission.delete()

#             messages.success(request, "Hisobotingiz muvaqqatiyatli o'chirildi.")
#         except Submission.DoesNotExist:
#             messages.info(request, "Hisobot maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            
#         return redirect('dashboard:submissions')


# class WorksView(IsCeoOrManager, View):

#     def get(self, request: HttpRequest) -> HttpResponse:

#         works = Submission.objects.order_by('-submitted_at')
#         ctx = {
#             'works': works
#         }
#         if request.user.role == User.MANAGER:
#             ctx['kpis'] = KPI.objects.filter(responsible_employee=request.user)
#         return render(request, 'dashboard/works/list.html', ctx)


# class WorkDetailView(IsCeoOrManager, View):

#     def get(self, request: HttpRequest, work_id: int) -> HttpResponse:
        
#         try:
#             submission = Submission.objects.get(id=work_id)
#             submission.is_checked = True
#             submission.save()

#         except Submission.DoesNotExist:
#             messages.info(request, "Hisobot maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")

#         ctx = {
#             'work': submission
#         }
#         if request.user.role == User.MANAGER:
#             ctx['kpis'] = KPI.objects.filter(responsible_employee=request.user)
#         return render(request, 'dashboard/works/detail.html', ctx)


# class AssessmentView(IsManager, View):

#     def post(self, request: HttpRequest, work_id: int) -> HttpResponse:
        
#         try:
#             submission = Submission.objects.get(id=work_id)

#         except Submission.DoesNotExist:
#             messages.info(request, "Hisobot maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
#             return redirect("dashboard:works")

#         update_form = MarkForm(request.POST, instance=submission.mark)
#         if update_form.is_valid():
#             update_form.save()
#             submission.is_marked = True
#             submission.save()

#             messages.success(request, "Hisobotni muvaffaqiyatli baholadingiz.")
#             return redirect("dashboard:works")

#         messages.info(request, "Hisobot maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
#         return redirect("dashboard:works")
