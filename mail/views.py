import datetime
from time import strftime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.cache import cache
from django.views import View

from config.settings import CACHE_ENABLED, CACHE_TIME
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from .models import Customer, Message, Attempt, Newsletter
from .forms import CustomerForm, MessageForm, NewsletterForm
from .servises import MailService


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
                messages = Message.objects.filter(owner=user)
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


class NewsletterListView(LoginRequiredMixin, ListView):
    """Класс представления списка рассылок"""

    model = Newsletter
    template_name = "newsletters_list.html"
    context_object_name = "newsletters"

    def get_queryset(self):
        """Метод получения доступных рассылок"""

        user = self.request.user

        if user.has_perm("mail.can_view_all"):
            if CACHE_ENABLED:
                newsletters = cache.get("newsletters_list_all")
                if not newsletters:
                    newsletters = super().get_queryset()
                    cache.set("newsletters_list_all", newsletters, CACHE_TIME)
                return newsletters
            return super().get_queryset()

        if CACHE_ENABLED:
            newsletters = cache.get(f"newsletters_list_{user.id}")
            if not newsletters:
                newsletters = Newsletter.objects.filter(owner=user)
                cache.set(f"messages_list_{user.id}", newsletters, CACHE_TIME)
            return newsletters
        return Newsletter.objects.filter(owner=user)


class NewsletterDetailView(LoginRequiredMixin, View):
    """Класс представления одной рассылки"""

    def get(self, request, pk):

        newsletter = Newsletter.objects.get(id=pk)
        context = {"newsletter": newsletter}
        user = self.request.user
        if not (user == newsletter.owner or user.has_perm("mail.can_view_all")):
            raise PermissionDenied
        return render(request, "detail_newsletter.html", context=context)

    def post(self, request, pk):
        newsletter = Newsletter.objects.get(id=pk)
        customers = newsletter.customers.all()
        user = self.request.user
        if not user.has_perm("mail.can_send_newsletters"):
            raise PermissionDenied
        MailService.send_email(customers, newsletter, user)
        context = {"newsletter": newsletter}
        return render(request, "newsletter_start.html", context=context)


    # def get_object(self, queryset=None):
    #     """Метод получения объекта рассылки"""
    #
    #     newsletter = super().get_object()
    #     user = self.request.user
    #     if not (user == newsletter.owner or user.has_perm("mail.can_view_all")):
    #         raise PermissionDenied
    #
    #     return newsletter


class NewsletterCreateView(CreateView):
    """Класс представления создания рассылки"""

    model = Newsletter
    form_class = NewsletterForm
    template_name = "edit_newsletter.html"
    success_url = reverse_lazy('mail:newsletters_list')

    def form_valid(self, form):
        """Метод валидации формы создания"""

        user = self.request.user
        if not user.has_perm("mail.add_newsletter"):
            raise PermissionDenied
        newsletter = form.save()
        newsletter.owner = user
        newsletter.save()
        return super().form_valid(form)


class NewsletterUpdateView(UpdateView):
    """Класс представления редактирования рассылки"""

    model = Newsletter
    form_class = NewsletterForm
    template_name = "edit_newsletter.html"
    success_url = reverse_lazy('mail:newsletters_list')

    def form_valid(self, form):
        """Метод валидации формы создания"""

        user = self.request.user
        if not user.has_perm("mail.change_newsletter"):
            raise PermissionDenied
        return super().form_valid(form)


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    """Класс представления удаления рассылки"""

    model = Newsletter
    template_name = "delete_newsletter.html"
    success_url = reverse_lazy('mail:newsletters_list')

    def get_object(self, queryset=None):
        """Метод получения объекта рассылки"""

        newsletter = super().get_object()
        user = self.request.user
        if not (user == newsletter.owner or user.has_perm("mail.delete_newsletter")):
            raise PermissionDenied

        return newsletter

    def form_valid(self, form):
        """Метод проверяет наличие прав перед удалением"""

        user = self.request.user
        if not (user == self.object.owner or user.has_perm("mail.delete_newsletter")):
            raise PermissionDenied
        return super().form_valid(form)


class AttemptListView(LoginRequiredMixin, ListView):
    """Класс представления списка рассылок"""

    model = Attempt
    template_name = "attempts_list.html"
    context_object_name = "attempts"

    def get_queryset(self):
        """Метод получения доступных рассылок"""

        user = self.request.user

        if user.has_perm("mail.can_view_all"):
            if CACHE_ENABLED:
                attempts = cache.get("attempts_list_all")
                if not attempts:
                    attempts = super().get_queryset()
                    cache.set("attempts_list_all", attempts, CACHE_TIME)
                return attempts
            return super().get_queryset()

        if CACHE_ENABLED:
            attempts = cache.get(f"attempts_list_{user.id}")
            if not attempts:
                attempts = Attempt.objects.filter(owner=user)
                cache.set(f"attempts_list_{user.id}", attempts, CACHE_TIME)
            return attempts
        return Attempt.objects.filter(owner=user)
