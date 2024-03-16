from django.urls import path
from . import views

urlpatterns = [
    # messaging

path('message-list', views.message_list, name='message-list'),

path('message-detail/<int:pk>/', views.message_detail, name='message-detail'),

path('create-message/<slug:product_slug>/', views.create_message, name='create-message'),

path('delete-message/<int:message_id>/', views.delete_message, name='delete_message'),


]