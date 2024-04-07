from django.urls import path
from . import views

urlpatterns = [
    
# messaging

path('message-list', views.message_list, name='message-list'),

path('create-message/<slug:product_slug>/', views.create_message, name='create-message'),

path('delete-message/<int:conversation_id>/', views.delete_conversation, name='delete-message'),

path('mark-conversation-messages-read/<int:conversation_id>/', views.mark_conversation_messages_read, name='mark-conversation-messages-read'),
]