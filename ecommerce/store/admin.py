from django.contrib import admin
from .models import Category, Product, Images
from messaging.models import Message, Conversation
from django.apps import apps

# Custom admin classes for each model
class CategoryAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    pass

class ImagesAdmin(admin.ModelAdmin):
    pass

class ConversationsAdmin(admin.ModelAdmin):
    pass

class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'subject', 'created_at']
    search_fields = ['sender__username', 'receiver__username', 'subject']
    list_filter = ['created_at','sender__username', 'receiver__username', 'subject']

# Register custom admin classes for each model
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Conversation,ConversationsAdmin)
# Define custom admin groups and assign permissions
from django.contrib.auth.models import Group, Permission

# Create or get the admin group
admin_group, created = Group.objects.get_or_create(name='Admin')

# Get permissions for all models
# Get all installed apps
installed_apps = apps.get_app_configs()

# List to store all permissions
all_permissions = []

# Loop through each installed app
for app in installed_apps:
    # Get all permissions for the current app
    permissions = Permission.objects.filter(content_type__app_label=app.label)
    # Extend the list of all_permissions with permissions for the current app
    all_permissions.extend(permissions)

# Assign all permissions to the admin group
admin_group.permissions.set(all_permissions)

# Create or get the staff admin group
staff_admin_group, created = Group.objects.get_or_create(name='Staff Admin')

# Assign permissions for limited CRUD operations to the staff admin group
# Example: Only allow adding and changing products
staff_admin_group.permissions.set([
    Permission.objects.get(codename='add_product'),
    Permission.objects.get(codename='change_product'),
])

# Assign users to the appropriate groups based on their roles
from django.contrib.auth.models import User

# Get or create users
admin_user, created = User.objects.get_or_create(username='admin')
staff_admin_user, created = User.objects.get_or_create(username='staff_admin')

# Assign users to groups
admin_user.groups.add(admin_group)
staff_admin_user.groups.add(staff_admin_group)
