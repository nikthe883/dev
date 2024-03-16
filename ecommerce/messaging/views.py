from django.shortcuts import redirect, render, get_object_or_404,HttpResponse
from .forms import MessageForm
from store.models import Product
from .models import Message
from django.http import JsonResponse
from django.contrib import messages
import json

def create_message(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    if request.method == 'POST':
        if 'application/json' in request.content_type:
            # Parse the JSON data from the request body
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)
            
            # Create a MessageForm instance with the parsed data
            print(data)
            form = MessageForm(data)
        else:
            # For form-encoded POST requests
            form = MessageForm(request.POST)
       
        

        if form.is_valid():
            message_instance = form.save(commit=False)
            message_instance.sender = request.user  # Assign the current user as the sender
            message_instance.product = product
            
            message_instance.receiver = product.user  # Assign the product's user as the receiver
            message_instance.save()
            messages.success(request, 'Message send successfully')
            return redirect('dashboard')
        else:	
            messages.error(request, 'Message not send successfully')

    else:
        form = MessageForm()

    return render(request, 'messages/create-message.html', {'form': form})


def message_list(request):
    current_user = request.user
    unread_messages = (
        Message.objects
        .filter(receiver=current_user, read=False)
        .order_by('-created_at')
        .select_related('product', 'sender')
    )
    read_messages = (
        Message.objects
        .filter(receiver=current_user, read=True)
        .order_by('-created_at')
        .select_related('product', 'sender')
    )
    all_messages = list(unread_messages) + list(read_messages)
    
    grouped_messages = {}
    for message in all_messages:
        key = (message.sender.username, message.product.title)
        if key not in grouped_messages:
            grouped_messages[key] = []
        grouped_messages[key].append(message)

   

    return render(request, 'messages/message-list.html', {'grouped_messages': grouped_messages})


def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    message.read = True
    message.save()
    return JsonResponse({'status': 'success'})

def delete_message(request, message_id):
    try:
        message = Message.objects.get(pk=message_id)
        message.delete()
        messages.success(request, 'Message deleted successfully')
    except Message.DoesNotExist:
        messages.error(request, 'Message not found')

    return JsonResponse({'status': 'ok'})  # Return a JSON response

