from django.contrib.auth.views import (LogoutView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy
from django.views.decorators.cache import cache_page

from config.settings import CACHE_TIME
from users.apps import UsersConfig

from .views import (CustomUserCreateView, CustomUserDetailManagerView,
                    CustomUserDetailView, CustomUserEmailConfirm,
                    CustomUserListView, CustomUserLoginView,
                    CustomUserUpdateManagerView, CustomUserUpdateView)

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
    path('password-reset/',
         PasswordResetView.as_view(
             template_name="password_reset.html",
             email_template_name="password_reset_email.html",
             success_url=reverse_lazy("users:password_reset_done")
         ),
         name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="password_reset_confirm.html",
             success_url=reverse_lazy("users:password_reset_complete")
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name='password_reset_complete'),
]
