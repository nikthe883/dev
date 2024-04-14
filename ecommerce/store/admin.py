from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category, Product, Images, ProductReview
from django.contrib.auth.models import Group, Permission
from messaging.models import Message, Conversation
from django.apps import apps

class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1

class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 1


# Custom admin classes for each model
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    """

    prepopulated_fields = {'slug': ('name',)}  # Automatically generate slug from name
    list_display = ['name', 'slug', 'parent']
    search_fields = ['name']
    list_filter = ['parent']

class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.
    """

    prepopulated_fields = {'slug': ('title',)}  # Automatically generate slug from title
    list_display = ['title', 'brand', 'category', 'price', 'user']
    search_fields = ['title', 'brand', 'category__name']
    list_filter = ['category']
    inlines = [ImagesInline, ProductReviewInline]

class ImagesAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Images model.
    """

    list_display = ['product', 'image']
    search_fields = ['product__title']

class ConversationsAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Conversation model.
    """

    list_display = ['id', 'participants_list']
    search_fields = ['participants__username']

    def participants_list(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    participants_list.short_description = "Participants"

class MessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Message model.
    """

    list_display = ['sender', 'receiver', 'subject', 'created_at', 'conversation']
    search_fields = ['sender__username', 'receiver__username', 'subject', 'conversation__id']
    list_filter = ['created_at', 'sender__username', 'receiver__username', 'conversation']
    date_hierarchy = 'created_at'

class ProductReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ProductReview model.
    """
    
    list_display = ['product', 'author', 'rating', 'created_at']
    search_fields = ['product__title', 'author__username']
    list_filter = ['created_at', 'rating']

# Register custom admin classes for each model
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Conversation,ConversationsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)


