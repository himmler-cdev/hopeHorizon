
from django.db import migrations

def add_user_roles(apps, schema_editor):
    UserRole = apps.get_model('backend', 'UserRole')
    UserRole.objects.create(role='User')
    UserRole.objects.create(role='Therapist')
    UserRole.objects.create(role='Moderator')


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_user_roles),
    ]