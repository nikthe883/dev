from django.db import models

from django.contrib.auth.models import User
from store.models import Product

class Message(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="messages", null=True, blank=True)

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name
