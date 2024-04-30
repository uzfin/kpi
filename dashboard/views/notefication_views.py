from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from users.permissions import IsCeoOrManager
from dashboard.forms import NoteficationCreationForm
from dashboard.models import Notefication

from users.models import User


class SendNoteficationView(IsCeoOrManager, View):

    def get(self, request: HttpRequest, employee_id: int) -> HttpResponse:

        try:
            employee = User.objects.get(id=employee_id)
        except User.DoesNotExist: 
            messages.info(request, "Hodim maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")

            return redirect('dashboard:departments')

        ctx = {
            "employee": employee,
            "notefication": Notefication
        }

        return render(request, 'dashboard/notefications/send.html', ctx)

    def post(self, request: HttpRequest, employee_id: int) -> HttpResponse:

        create_form = NoteficationCreationForm(request.POST)
        print(request.POST)
        print(create_form.errors)

        if create_form.is_valid():
            create_form.save()
            messages.success(request, "Xabar hodimga muvaffaqiyatli yuborildi.")
            return redirect('dashboard:departments')
        else:
            messages.info(request, "Xabar maʼlumotlarda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return redirect('dashboard:departments')
