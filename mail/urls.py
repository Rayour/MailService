from django.urls import path
from django.views.decorators.cache import cache_page

from config.settings import CACHE_TIME
from mail.apps import MailConfig
from mail.views import (AttemptListView, CustomerCreateView,
                        CustomerDeleteView, CustomerDetailView,
                        CustomerListView, CustomerUpdateView,
                        MessageCreateView, MessageDeleteView,
                        MessageDetailView, MessageListView, MessageUpdateView,
                        NewsletterCreateView, NewsletterDeleteView,
                        NewsletterDetailView, NewsletterListView,
                        NewsletterUpdateView)

app_name = MailConfig.name

urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='customers_list'),
    path('create_customer/', CustomerCreateView.as_view(), name='create_customer'),
    path('edit_customer/<int:pk>', CustomerUpdateView.as_view(), name='edit_customer'),
    path('detail_customer/<int:pk>', cache_page(CACHE_TIME)(CustomerDetailView.as_view()), name='detail_customer'),
    path('delete_customer/<int:pk>', CustomerDeleteView.as_view(), name='delete_customer'),
    path('messages/', MessageListView.as_view(), name='messages_list'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('edit_message/<int:pk>', MessageUpdateView.as_view(), name='edit_message'),
    path('detail_message/<int:pk>', cache_page(CACHE_TIME)(MessageDetailView.as_view()), name='detail_message'),
    path('delete_message/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),
    path('newsletters/', NewsletterListView.as_view(), name='newsletters_list'),
    path('create_newsletter/', NewsletterCreateView.as_view(), name='create_newsletter'),
    path('edit_newsletter/<int:pk>', NewsletterUpdateView.as_view(), name='edit_newsletter'),
    path('detail_newsletter/<int:pk>', cache_page(CACHE_TIME)(NewsletterDetailView.as_view()),
         name='detail_newsletter'),
    path('delete_newsletter/<int:pk>', NewsletterDeleteView.as_view(), name='delete_newsletter'),
    path('attempts/', AttemptListView.as_view(), name='attempts_list'),
]
