from django.shortcuts import redirect, render, get_object_or_404,HttpResponse
from .forms import MessageForm
from store.models import Product
from .models import Message
from django.http import JsonResponse

def create_message(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    if request.method == 'POST':

        form = MessageForm(request.POST)

        if form.is_valid():
        
            message_instance = form.save(commit=False)
            message_instance.sender = request.user  # Assign the current user as the sender
            message_instance.product = product
            
            message_instance.receiver = product.user  # Assign the product's user as the receiver
            message_instance.save()
           
            return redirect('dashboard')
        else:	
            print(form.errors)

    else:
        form = MessageForm()

    return render(request, 'messages/create-message.html', {'form': form})


def message_list(request):
    current_user = request.user.id
    unread_messages = Message.objects.filter(receiver=current_user, read=False).order_by('-created_at').select_related('product')
    read_messages = Message.objects.filter(receiver=current_user, read=True).order_by('-created_at').select_related('product')
    messages = list(unread_messages) + list(read_messages)
    return render(request, 'messages/message-list.html', {'messages': messages})

def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    message.read = True
    message.save()
    return JsonResponse({'status': 'success'})

