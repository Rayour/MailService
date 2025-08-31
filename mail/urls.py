from django.contrib import admin
from django.urls import path, include
from mail.apps import MailConfig
from mail.views import CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDetailView, CustomerDeleteView, MessageCreateView, MessageDeleteView, MessageDetailView, MessageUpdateView, MessageListView

app_name = MailConfig.name

urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='customers_list'),
    path('create_customer/', CustomerCreateView.as_view(), name='create_customer'),
    path('edit_customer/<int:pk>', CustomerUpdateView.as_view(), name='edit_customer'),
    path('detail_customer/<int:pk>', CustomerDetailView.as_view(), name='detail_customer'),
    path('delete_customer/<int:pk>', CustomerDeleteView.as_view(), name='delete_customer'),
    path('messages/', MessageListView.as_view(), name='messages_list'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('edit_message/<int:pk>', MessageUpdateView.as_view(), name='edit_message'),
    path('detail_message/<int:pk>', MessageDetailView.as_view(), name='detail_message'),
    path('delete_message/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),
]