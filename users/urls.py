from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from users.apps import UsersConfig

from .views import CustomUserCreateView, CustomUserEmailConfirm, CustomUserLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', CustomUserCreateView.as_view(), name='register'),
    path('login/', CustomUserLoginView.as_view(template_name='login.html'), name='login'),
    path('mail_confirm/', CustomUserEmailConfirm.as_view(), name='mail_confirm'),
]
