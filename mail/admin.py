from django.contrib import admin

from .models import Customer, Message, Newsletter, Attempt


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name")
    search_fields = ("email", "full_name")
    list_filter = ("owner",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "topic")
    list_filter = ("owner",)
    search_fields = ("topic",)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "message", "owner")
    list_filter = ("owner", "status")


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "customer", "message", "server_response", "owner")
    list_filter = ("owner", "status")
