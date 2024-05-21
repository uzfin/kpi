from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.permissions import IsEmployee, IsManager, IsStaff
from dashboard.forms import SubmissionCreationForm, SubmissionUpdationForm
from dashboard.models import Submission, Clause, KPI
from users.models import User


class SubmissionsView(IsStaff, View):

    def get(self, request: HttpRequest, kpi_id: int) -> HttpResponse:
        user = request.user
        try:
            current_kpi = KPI.objects.get(id=kpi_id)
        except KPI.DoesNotExist:
            messages.info(request, "KPI ma'lumotlarida xatolik yuz berdi.")
            return redirect("dashboard:main")

        if user.role == User.EMPLOYEE:
            submissions = user.submissions.filter(kpi=current_kpi).order_by("-updated_at")
        elif user.role == User.MANAGER:
            submissions = Submission.objects.filter(kpi=current_kpi, kpi__responsible_person=user).order_by("-updated_at")
        elif user.role == User.BOSS:
            submissions = Submission.objects.filter(kpi=current_kpi).order_by("-updated_at")
        else:
            submissions = []

        ctx = {
            "submissions": submissions
        }

        return render(request, 'dashboard/submissions/list.html', ctx)


class SubmissionCreateView(IsEmployee, View):

    def get(self, request: HttpRequest, clause_id: int) -> HttpResponse:
        try:
            clause = Clause.objects.get(id=clause_id)
        except Clause.DoesNotExist:
            messages.info(request, "Band maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:clause-detail', clause_id=clause_id)

        ctx = {
            "clause": clause,
        }
        try:
            submission = request.user.submissions.get(clause=clause)
            
            messages.info(request, "Ushbu band bo'yicha hisobot yuborgansiz.")
            return redirect("dashboard:submission-detail", submission_id=submission.id)
        except:
            pass

        return render(request, 'dashboard/submissions/create.html', ctx)

    def post(self, request: HttpRequest, clause_id: int) -> HttpResponse:
        try:
            clause = Clause.objects.get(id=clause_id)
        except Clause.DoesNotExist:
            messages.info(request, "Band maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:clause-detail', clause_id=clause_id)

        create_form = SubmissionCreationForm(request.POST, request.FILES)

        if create_form.is_valid():
            instance = create_form.instance

            instance.save()

            messages.success(request, "Hisobotingiz muvaffaqiyatli joylandi.")
            return redirect('dashboard:main')

        else:
            messages.info(request, "Ishingizni joylashda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring. Oldin joylagan bo'lishingiz mumkin.")
            return redirect('dashboard:main')


class SubmissionDetailView(IsEmployee, View):

    def get(self, request: HttpRequest, submission_id: int) -> HttpResponse:

        try:
            submission = request.user.submissions.get(id=submission_id)
        except Submission.DoesNotExist:
            messages.info(request, "Hisobot maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')

        ctx = {
            "submission": submission,
        }

        return render(request, 'dashboard/submissions/detail.html', ctx)


class SubmissionUpdateView(IsEmployee, View):

    def get(self, request: HttpRequest, submission_id: int) -> HttpResponse:

        try:
            submission = request.user.submissions.get(id=submission_id)
        except Submission.DoesNotExist:
            messages.info(request, "Hisobot maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')

        ctx = {
            "submission": submission,
        }

        return render(request, 'dashboard/submissions/update.html', ctx)

    def post(self, request: HttpRequest, submission_id: int) -> HttpResponse:

        try:
            submission = request.user.submissions.get(id=submission_id)
        except Submission.DoesNotExist:
            messages.info(request, "Hisobot maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')

        update_form = SubmissionUpdationForm(request.POST, request.FILES, instance=submission)
        if update_form.is_valid():
            update_form.save()

            messages.success(request, "Hisobotingiz muvaffaqiyatli yangilandi.")
            return redirect("dashboard:main")

        ctx = {
            "submission": submission,
        }
        messages.info(request, "Hisobotingizni yangilashda xatolik yuz berdi. Iltimos, yana bir bor uninib ko'ring.")
        return render(request, 'dashboard/submissions/update.html', ctx)


class SubmissionDeleteView(IsEmployee, View):

    def get(self, request: HttpRequest, submission_id: int) -> HttpResponse:

        try:
            submission = request.user.submissions.get(id=submission_id)
            submission.delete()

            messages.success(request, "Hisobotingiz muvaqqatiyatli o'chirildi.")
        except Submission.DoesNotExist:
            messages.info(request, "Hisobot maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            
        return redirect('dashboard:main')


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
