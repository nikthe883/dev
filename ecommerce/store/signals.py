from django.contrib.auth.models import Group, Permission, User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password

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
    
    # Ensure the admin user exists
    admin_user, created = User.objects.get_or_create(username='super_admin')
    if created:
        admin_user.email = 'super_admin@example.com'
        admin_user.password = make_password('nikola12A')  
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
    admin_group.user_set.add(admin_user)

    # Ensure the staff admin user exists
    staff_admin_user, created = User.objects.get_or_create(username='staff_admin')
    if created:
        staff_admin_user.email = 'staff_admin@example.com'
        staff_admin_user.password = make_password('nikola12A')  
        staff_admin_user.is_staff = True
        staff_admin_user.save()
    staff_admin_group.user_set.add(staff_admin_user)
