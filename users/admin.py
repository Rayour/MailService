from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "last_name", "first_name")
    search_fields = ("email", "last_name")
