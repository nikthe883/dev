from django import forms
from .models import Message



# Message form
class MessageForm(forms.ModelForm):
    class Meta:
         model = Message
         fields = ['subject', 'body']

