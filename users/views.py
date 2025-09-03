import datetime
import logging
import os
import random
import string
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.core.cache import cache

from config.settings import DEFAULT_FROM_EMAIL, HOST_NAME, CACHE_ENABLED, CACHE_TIME, BASE_DIR

from .forms import CustomUserChangeForm, CustomUserCreationForm, CustomAuthForm, CustomUserChangeManagerForm
from .models import CustomUser
from mail.models import Newsletter, Customer, Attempt

User = get_user_model()
date_today = datetime.datetime.today().strftime("%d-%m-%Y")
file_name = f"{date_today}_logs.log"
log_path = os.path.join(BASE_DIR, "logs", file_name)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=log_path,
    filemode="a",
    encoding="utf-8",
)
logger = logging.getLogger("users_views")


class CustomUserCreateView(CreateView):
    """Класс представления для создания пользователя"""

    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        logger.info(f"Создан пользователь {user}")
        group = Group.objects.get(name="Base_user")
        user.groups.add(group)
        logger.info(f"Пользователь {user} добавлен в группу доступа 'Base_user'")
        user.hash = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        user.save()
        login(self.request, user)
        self.send_welcome_email(user.email, user.hash)
        logger.info(f"Пользователю {user} отправлено письмо для подтверждения почты {user.email}")
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
        user = self.request.user
        logger.info(f"Пользователь {user} отредактировал свой профиль")
        return user


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
        logger.info(f"Пользователь {user} зашел в свой профиль")
        if user.has_perm("users.can_manage"):
            logger.info(f"Пользователь {user} получил статистику по рассылкам всех пользователей")
            newsletters_all = Newsletter.objects.count()
            newsletters_active = Newsletter.objects.filter(status="started").count()
            unique_customers = Customer.objects.values('email').distinct().count()
        else:
            logger.info(f"Пользователь {user} получил статистику по своим рассылкам")
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
                logger.info(f"Пользователь {user} подтвердил электронную почту")
            else:
                logger.warning("Ошибочное подтверждение электронной почты")
                context = {"message": "К сожалению пользователь не найден, пожалуйста, перейдите по ссылке из письма"}

        return render(request, "mail_confirm.html", context=context)


class CustomUserLoginView(LoginView):
    """Класс представления логина пользователя"""

    template_name = 'login.html'
    authentication_form = CustomAuthForm

    def form_valid(self, form):

        user = form.get_user()
        if user and not user.is_mail_confirmed:
            form.add_error("username", "Электронная почта не подтверждена")
            logger.warning(f"Пользователь {user} пытается войти в систему без подтверждения электронной почты")
            return self.form_invalid(form)
        logger.info(f"Пользователь {user} вошел в систему")
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
            logger.warning(f"Пользователь {user} не имеет прав на просмотр списка пользователей")
            raise PermissionDenied

        logger.info(f"Получение списка пользователй для менеджера {user}")
        if CACHE_ENABLED:
            users = cache.get(f"users_list")
            if not users:
                users = CustomUser.objects.filter(groups__name='Base_user')
                cache.set(f"users_list", users, CACHE_TIME)
                logger.info("Список пользователей записан в кеш")
            logger.info("Список пользователей получен из кеша")
            return users
        return CustomUser.objects.filter(groups__name='Base_user')


class CustomUserDetailManagerView(LoginRequiredMixin, View):
    """Класс представления для отображения профиля пользователя"""

    def get(self, request, pk):
        """Метод обработки гет запроса"""

        manager = self.request.user
        if not manager.has_perm("users.can_manage"):
            logger.warning(f"Пользователь {manager} не имеет прав на просмотр информации о пользователях системы")
            raise PermissionDenied

        user = CustomUser.objects.get(id=pk)
        logger.info(f"Получение статистики по пользователю {user} по запросу {manager}")
        success_attempts = Attempt.objects.filter(owner=user, status="success").count()
        fail_attempts = Attempt.objects.filter(owner=user, status="fail").count()
        finished_newsletters = Newsletter.objects.filter(owner=user, status="finished").count()

        context = {
            "user": user,
            "success_attempts": success_attempts,
            "fail_attempts": fail_attempts,
            "finished_newsletters": finished_newsletters,
        }
        return render(request, "detail_user.html", context=context)
