from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.permissions import IsACM, IsEmployee, IsCMB
from dashboard.forms import NoteficationCreationForm
from dashboard.models import Notefication, KPI

from users.models import User


class SendNoteficationView(IsCMB, View):

    def get(self, request: HttpRequest, employee_id: int) -> HttpResponse:

        try:
            employee = User.objects.get(id=employee_id)
        except User.DoesNotExist: 
            messages.info(request, "Hodim maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")

            return redirect('dashboard:departments')

        ctx = {
            "employee": employee,
            "department": request.user.departments.first(),
            "notefication": Notefication,
        }

        return render(request, 'dashboard/notefications/send.html', ctx)

    def post(self, request: HttpRequest, employee_id: int) -> HttpResponse:

        create_form = NoteficationCreationForm(request.POST)

        if create_form.is_valid():
            create_form.save()
            messages.success(request, "Xabar hodimga muvaffaqiyatli yuborildi.")
            return redirect('dashboard:main')
        else:
            messages.info(request, "Xabar maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:main')


class NoteficationView(IsEmployee, View):

    def get(self, request: HttpRequest) -> HttpResponse:

        ctx = {
            "all_notefications": request.user.notefications.order_by("-updated_at"),
            "root_notefication": Notefication,
        }

        return render(request, 'dashboard/notefications/list.html', ctx)


class SeeNoteficationView(IsEmployee, View):

    def get(self, request: HttpRequest, notefication_id: int) -> HttpResponse:

        try:
            notefication = request.user.notefications.get(id=notefication_id)
            notefication.unread = False
            notefication.save()
        except Notefication.DoesNotExist: 
            messages.info(request, "Xabar maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")

            return redirect('dashboard:get-notefications')

        ctx = {
            "notefication": notefication,
            "root_notefication": Notefication,
        }

        return render(request, 'dashboard/notefications/detail.html', ctx)