from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.cache import cache

from config.settings import CACHE_ENABLED, CACHE_TIME
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from .models import Customer, Message, Attempt, Newsletter
from .forms import CustomerForm, MessageForm


class CustomerListView(LoginRequiredMixin, ListView):
    """Класс представления списка клиентов"""

    model = Customer
    template_name = "customers_list.html"
    context_object_name = "customers"

    def get_queryset(self):
        """Метод получения доступных клиентов"""

        user = self.request.user

        if user.has_perm("mail.can_view_all"):
            if CACHE_ENABLED:
                customers = cache.get("customers_list_all")
                if not customers:
                    customers = super().get_queryset()
                    cache.set("customers_list_all", customers, CACHE_TIME)
                return customers
            return super().get_queryset()

        if CACHE_ENABLED:
            customers = cache.get(f"customers_list_{user.id}")
            if not customers:
                customers = Customer.objects.filter(owner=user)
                cache.set(f"customers_list_{user.id}", customers, CACHE_TIME)
            return customers
        return Customer.objects.filter(owner=user)


class CustomerDetailView(LoginRequiredMixin, DetailView):
    """Класс представления одного клиентов"""

    model = Customer
    template_name = "detail_customer.html"
    context_object_name = "customer"

    def get_object(self, queryset=None):
        """Метод получения объекта клиента"""

        customer = super().get_object()
        user = self.request.user
        if not (user == customer.owner or user.has_perm("mail.can_view_all")):
            raise PermissionDenied

        return customer


class CustomerCreateView(CreateView):
    """Класс представления создания клиентов"""

    model = Customer
    form_class = CustomerForm
    template_name = "edit_customer.html"
    success_url = reverse_lazy('mail:customers_list')

    def form_valid(self, form):
        """Метод валидации формы создания"""

        user = self.request.user
        if not user.has_perm("mail.add_customer"):
            raise PermissionDenied
        customer = form.save()
        customer.owner = user
        customer.save()
        return super().form_valid(form)


class CustomerUpdateView(UpdateView):
    """Класс представления редактирования клиентов"""

    model = Customer
    form_class = CustomerForm
    template_name = "edit_customer.html"
    success_url = reverse_lazy('mail:customers_list')

    def form_valid(self, form):
        """Метод валидации формы создания"""

        user = self.request.user
        if not user.has_perm("mail.change_customer"):
            raise PermissionDenied
        return super().form_valid(form)


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    """Класс представления удаления клиента"""

    model = Customer
    template_name = "delete_customer.html"
    success_url = reverse_lazy('mail:customers_list')

    def get_object(self, queryset=None):
        """Метод получения объекта клиента"""

        customer = super().get_object()
        user = self.request.user
        if not (user == customer.owner or user.has_perm("mail.delete_customer")):
            raise PermissionDenied

        return customer

    def form_valid(self, form):
        """Метод проверяет наличие прав перед удалением"""

        user = self.request.user
        if not (user == self.object.owner or user.has_perm("mail.delete_customer")):
            raise PermissionDenied
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    """Класс представления списка писем"""

    model = Message
    template_name = "messages_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        """Метод получения доступных писем"""

        user = self.request.user

        if user.has_perm("mail.can_view_all"):
            if CACHE_ENABLED:
                messages = cache.get("messages_list_all")
                if not messages:
                    messages = super().get_queryset()
                    cache.set("messages_list_all", messages, CACHE_TIME)
                return messages
            return super().get_queryset()

        if CACHE_ENABLED:
            messages = cache.get(f"messages_list_{user.id}")
            if not messages:
                customers = Message.objects.filter(owner=user)
                cache.set(f"messages_list_{user.id}", messages, CACHE_TIME)
            return messages
        return Message.objects.filter(owner=user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Класс представления одного письма"""

    model = Message
    template_name = "detail_message.html"
    context_object_name = "message"

    def get_object(self, queryset=None):
        """Метод получения объекта письма"""

        message = super().get_object()
        user = self.request.user
        if not (user == message.owner or user.has_perm("mail.can_view_all")):
            raise PermissionDenied

        return message


class MessageCreateView(CreateView):
    """Класс представления создания письма"""

    model = Message
    form_class = MessageForm
    template_name = "edit_message.html"
    success_url = reverse_lazy('mail:messages_list')

    def form_valid(self, form):
        """Метод валидации формы создания"""

        user = self.request.user
        if not user.has_perm("mail.add_message"):
            raise PermissionDenied
        message = form.save()
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    """Класс представления редактирования письма"""

    model = Message
    form_class = MessageForm
    template_name = "edit_message.html"
    success_url = reverse_lazy('mail:messages_list')

    def form_valid(self, form):
        """Метод валидации формы создания"""

        user = self.request.user
        if not user.has_perm("mail.change_message"):
            raise PermissionDenied
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Класс представления удаления письма"""

    model = Message
    template_name = "delete_message.html"
    success_url = reverse_lazy('mail:messages_list')

    def get_object(self, queryset=None):
        """Метод получения объекта письма"""

        message = super().get_object()
        user = self.request.user
        if not (user == message.owner or user.has_perm("mail.delete_message")):
            raise PermissionDenied

        return message

    def form_valid(self, form):
        """Метод проверяет наличие прав перед удалением"""

        user = self.request.user
        if not (user == self.object.owner or user.has_perm("mail.delete_message")):
            raise PermissionDenied
        return super().form_valid(form)
