from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_roles_and_admin(apps, schema_editor):
    Role = apps.get_model('users', 'Role')
    User = apps.get_model('users', 'User')

    reader_role, _ = Role.objects.get_or_create(role_name='Читатель')
    librarian_role, _ = Role.objects.get_or_create(role_name='Библиотекарь')
    admin_role, _ = Role.objects.get_or_create(role_name='Администратор')

    if not User.objects.filter(email='admin@example.com').exists():
        admin_user = User(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            role=admin_role,
            is_active=True,
            is_staff=True,
            password=make_password('123')
        )
        admin_user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_roles_and_admin),
    ]
