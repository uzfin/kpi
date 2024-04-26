from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, JsonResponse, HttpResponse

from .client import oAuth2Client
from core.settings import (
    CLIENT_SECRET,
    CLIENT_ID,
    REDIRECT_URI,
    RESOURCE_OWNER_URL,
    TOKEN_URL,
    AUTHORIZE_URL,
)

from users.forms import UserCreateForm


class RegisterView(View):
    def get(self, request):
        return render(request, "users/register.html")

    def post(self, request):
        create_form = UserCreateForm(request.POST, request.FILES)

        if create_form.is_valid():
            create_form.save()

            messages.success(request, "Siz muvaffaqiyatli ro'yxatdan o'tdingiz. Tizimga kirish uchun login va parol kiriting.")
            return redirect('users:login')
        else:
            messages.info(request, "Roʻyxatdan oʻtishda xatolik yuz berdi. Iltimos, yana bir bor urinib ko'ring.")
            return render(request, "users/register.html")


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)

            messages.success(request, "Siz muvaffaqiyatli tizimga kirdingiz.")

            return redirect("dashboard:main")
        else:
            messages.info(request, "Foydalanuvchi nomi yoki parol noto‘g‘ri. Iltimos, yana bir bor urinib ko'ring.")
            return render(request, "users/login.html")


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "Siz tizimdan muvaffaqiyatli chiqdingiz.")
        return redirect("users:login")


class OAuthAuthorizationView(View):

    def get(self, request: HttpRequest) -> JsonResponse:
        client = oAuth2Client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            authorize_url=AUTHORIZE_URL,
            token_url=TOKEN_URL,
            resource_owner_url=RESOURCE_OWNER_URL
        )
        authorization_url = client.get_authorization_url()
        return JsonResponse(
            {
                'authorization_url': authorization_url
            },
            status=200)


class OAuthCallbackView(View):

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        full_info = {}
        auth_code = self.kwargs.get('code')
        if not auth_code:
            return JsonResponse(
                {
                    'status': False,
                    'error': 'Authorization code is missing'
                },
                status=400)

        client = oAuth2Client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            authorize_url=AUTHORIZE_URL,
            token_url=TOKEN_URL,
            resource_owner_url=RESOURCE_OWNER_URL
        )
        access_token_response = client.get_access_token(auth_code)

        if 'access_token' in access_token_response:
            access_token = access_token_response['access_token']
            user_details = client.get_user_details(access_token)
            full_info['details'] = user_details
            full_info['token'] = access_token
            return JsonResponse(full_info, status=200)
        else:
            return JsonResponse(
                {
                    'status': False,
                    'error': 'Failed to obtain access token'
                },
                status=400
            )
