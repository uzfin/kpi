from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, JsonResponse, HttpResponse

from .client import oAuth2Client

from users.forms import UserCreateForm
from users.models import User


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
        return redirect("landing_page")


class AuthCallbackView(View):
    def get(self, request):

        code = request.GET.get('code')

        # checking code
        if code is None: return JsonResponse({'error': 'code is missing!'})

        # get access token and get user info
        client = oAuth2Client(
            client_id = settings.CLIENT_ID,
            client_secret = settings.CLIENT_SECRET,
            redirect_uri = settings.REDIRECT_URI,
            authorize_url = settings.AUTHORIZE_URL,
            token_url = settings.ACCESS_TOKEN_URL,
            resource_owner_url = settings.RESOURCE_OWNER_URL
        )
        access_token_response = client.get_access_token(code)

        if 'access_token' in access_token_response:
            access_token = access_token_response['access_token']
            user_details = client.get_user_details(access_token)

            # get user
            try:
                user = User.objects.get(username=user_details['login'])
            except User.DoesNotExist:
                user = User(
                    username=user_details['login'],
                    role=User.EMPLOYEE,
                )
                # set password
                if user_details['phone']:
                    user.set_password(raw_password=user_details['phone'])
                else:
                    user.set_password(raw_password='123456789')
                
                user.save()

            login(request, user)

            messages.info(request, 'Siz tizimdan muvaffaqiyatli ro\'yxatdan o\'tdingiz')
            messages.info(request, 'Siz hali biror bo\'limga biriktirilmagansiz shu sababli hamkasblaringiz mavjud emas!')
            return redirect('dashboard:main')
            
        else:
            messages.error(request, 'Kechirasiz hemis orqali kirishda xatolik yuz berdi. Iltimos yana bir bor urinib ko\'ring.')
            return redirect('landing_page')