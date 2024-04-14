from django.contrib.auth.models import Group, Permission, User
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def setup_groups_permissions(sender, **kwargs):
    # Setting up or getting groups
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    staff_admin_group, _ = Group.objects.get_or_create(name='Staff Admin')
    
    # Assigning permissions
    all_permissions = Permission.objects.all()
    admin_group.permissions.set(all_permissions)
    
    limited_permissions = Permission.objects.filter(codename__in=['add_product', 'change_product'])
    staff_admin_group.permissions.set(limited_permissions)
    
