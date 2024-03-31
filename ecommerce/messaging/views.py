from django.shortcuts import redirect, render, get_object_or_404,HttpResponse
from .forms import MessageForm
from store.models import Product
from .models import Message, Conversation
from django.http import JsonResponse
from django.contrib import messages
import json
from django.contrib.auth.models import User
from django.db.models import Q

from django.db import transaction
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

@transaction.atomic
def create_message(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    
    if request.method == 'POST':
        if 'application/json' in request.content_type:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)
       
            form = MessageForm(dict(list(data.items())[:2]))

            if form.is_valid():
                message_instance = form.save(commit=False)
                message_instance.sender = request.user
                message_instance.product = product
                
                # Fetch the User instance corresponding to the receiver's username
                receiver_username = list(data.values())[-1]
                
                receiver_user = User.objects.get(username=receiver_username)
                                # Create a conversation if it doesn't exist
                conversation = Conversation.objects.filter(participants=receiver_user).filter(participants=product.user).first()
                
                message_instance.receiver = receiver_user
                message_instance.conversation = conversation
                message_instance.save()
                
                messages.success(request, 'Message sent successfully')
                return JsonResponse({'status': 'ok'})
            else:
               
                messages.error(request, 'Message not sent successfully')
        else:
            form = MessageForm(request.POST)

            if form.is_valid():
                message_instance = form.save(commit=False)
                message_instance.sender = request.user
                message_instance.product = product
                message_instance.receiver = product.user
                conversation = Conversation.objects.filter(participants=request.user).filter(participants=product.user).first()

                if conversation is None:
                    # If no conversation exists, create a new one
                    conversation = Conversation.objects.create()
                    conversation.participants.add(request.user, product.user)
                message_instance.conversation = conversation
                
                message_instance.save()
                
                # Create a conversation between the sender and product user


                messages.success(request, 'Message sent successfully')
                return redirect(reverse_lazy('product-info', kwargs={'product_slug': product_slug}))
            else:
                messages.error(request, 'Message not sent successfully')

    else:
        form = MessageForm()

    return render(request, 'messages/create-message.html', {'form': form})



def message_list(request):
    current_user = request.user
    conversations = Conversation.objects.filter(participants=current_user)
    return render(request, 'messages/message-list.html', {'conversations': conversations})



def delete_conversation(request, conversation_id):
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.delete()
        messages.success(request, "Conversation deleted successfully.")
    except Message.DoesNotExist:
        messages.error(request, "Conversation does not exist.")

    return JsonResponse({'status': 'ok'})  # Return a JSON response

require_POST
def mark_conversation_messages_read(request, conversation_id):
    print(conversation_id)
    try:
        # Get the conversation
        conversation = Conversation.objects.get(pk=conversation_id)
        
        # Filter messages by conversation
        messages = conversation.messages.all()
        
        # Mark all messages as read
        for message in messages:
            if request.user == message.sender:
                message.read_sender = True
            elif request.user == message.receiver:
                message.read_receiver = True

            print(message.sender, message.receiver, message.read_sender,message.read_receiver)
            message.save()

        return JsonResponse({'success': True})  # Return success response
    except Conversation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Conversation not found'}, status=404)
