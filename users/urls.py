from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.decorators.cache import cache_page

from config.settings import CACHE_TIME
from users.apps import UsersConfig

from .views import CustomUserCreateView, CustomUserEmailConfirm, CustomUserLoginView, CustomUserDetailView, CustomUserUpdateView, CustomUserUpdateManagerView, CustomUserListView, CustomUserDetailManagerView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', CustomUserCreateView.as_view(), name='register'),
    path('login/', CustomUserLoginView.as_view(template_name='login.html'), name='login'),
    path('mail_confirm/', CustomUserEmailConfirm.as_view(), name='mail_confirm'),
    path('', CustomUserDetailView.as_view(), name='profile'),
    path('edit/', CustomUserUpdateView.as_view(), name='edit_profile'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('edit_user/<int:pk>/', CustomUserUpdateManagerView.as_view(), name='edit_user'),
    path('users_list/', CustomUserListView.as_view(), name='users_list'),
    path('detail_user/<int:pk>/', cache_page(CACHE_TIME)(CustomUserDetailManagerView.as_view()), name='detail_user'),
]
