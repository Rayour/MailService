import random
import string
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.core.cache import cache

from config.settings import DEFAULT_FROM_EMAIL, HOST_NAME, CACHE_ENABLED, CACHE_TIME

from .forms import CustomUserChangeForm, CustomUserCreationForm, CustomAuthForm, CustomUserChangeManagerForm
from .models import CustomUser
from mail.models import Newsletter, Customer

User = get_user_model()


class CustomUserCreateView(CreateView):
    """Класс представления для создания пользователя"""

    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name="Base_user")
        user.groups.add(group)
        user.hash = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        user.save()
        login(self.request, user)
        self.send_welcome_email(user.email, user.hash)
        return super().form_valid(form)

    def send_welcome_email(self, user_email, user_hash):
        subject = 'Подтверждение адреса электронной почты'
        message = f"""Спасибо, что проявили интерес к нашему сервису!
        Для завершения процесса регистрации подтвердите почту, перейдя по ссылке {HOST_NAME}users/mail_confirm/?hash={user_hash}"""
        from_email = DEFAULT_FROM_EMAIL
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    """Класс представления для редактирования пользователя"""

    model = User
    template_name = "edit_profile.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        """Метод получения пользователя"""
        return self.request.user


class CustomUserUpdateManagerView(LoginRequiredMixin, UpdateView):
    """Класс представления для редактирования пользователя"""

    model = User
    template_name = "edit_profile.html"
    form_class = CustomUserChangeManagerForm
    success_url = reverse_lazy("users:users_list")


class CustomUserDetailView(LoginRequiredMixin, View):
    """Класс представления для отображения профиля пользователя"""

    def get(self, request):
        """Метод обработки гет запроса"""

        user = self.request.user
        if user.has_perm("users.can_manage"):
            newsletters_all = Newsletter.objects.count()
            newsletters_active = Newsletter.objects.filter(status="started").count()
            unique_customers = Customer.objects.values('email').distinct().count()
        else:
            newsletters_all = Newsletter.objects.filter(owner=user).count()
            newsletters_active = Newsletter.objects.filter(owner=user, status="started").count()
            unique_customers = Customer.objects.filter(owner=user).values('email').distinct().count()
        context = {
            "user": user,
            "newsletters_all": newsletters_all,
            "newsletters_active": newsletters_active,
            "unique_customers": unique_customers,
        }
        return render(request, "profile.html", context=context)


class CustomUserEmailConfirm(View):
    """Класс представления подтверждения почты"""

    def get(self, request):
        """Метода для обработки GET запросов"""

        if self.request.GET.get('hash'):
            user = CustomUser.objects.get(hash=self.request.GET.get('hash'))
            if user:
                context = {"message": f"Добро пожаловать, {user.username}!"}
                user.is_mail_confirmed = True
                user.save()
            else:
                context = {"message": "К сожалению пользователь не найден, пожалуйста, перейдите по ссылке из письма"}

        return render(request, "mail_confirm.html", context=context)


class CustomUserLoginView(LoginView):
    """Класс представления логина пользователя"""

    template_name = 'login.html'
    authentication_form = CustomAuthForm

    def form_valid(self, form):

        user = form.get_user()
        print(user)
        if user and not user.is_mail_confirmed:
            form.add_error("username", "Электронная почта не подтверждена")
            return self.form_invalid(form)
        return super().form_valid(form)


class CustomUserListView(LoginRequiredMixin, ListView):
    """Класс представления списка пользователей"""

    model = CustomUser
    template_name = "users_list.html"
    context_object_name = "users"

    def get_queryset(self):
        """Метод получения списка пользователей"""

        user = self.request.user

        if not user.has_perm("users.can_manage"):
            raise PermissionError

        if CACHE_ENABLED:
            users = cache.get(f"users_list")
            if not users:
                # group = Group.objects.get(name='Base_user')
                users = CustomUser.objects.filter(groups__name='Base_user')
                cache.set(f"users_list", users, CACHE_TIME)
            return users
        return CustomUser.objects.filter(groups__name='Base_user')
