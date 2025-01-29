from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_users(apps, schema_editor):
    User = apps.get_model('backend', 'User')  # Adjust based on your app name
    UserRole = apps.get_model('backend', 'UserRole')  # Get the role model

    admin_role = UserRole.objects.last()  # Ensure at least one role exists
    user_role = UserRole.objects.first()  # Assume another role exists for regular users

    # Superuser
    User.objects.create(
        username='admin',
        email='admin@example.com',
        password=make_password('topsecret'),  
        is_superuser=True,
        is_staff=True,
        birthdate='2000-01-01',
        user_role_id=admin_role,
    )

    # Regular users
    users = [
        {"username": "user1", "email": "user1@example.com", "password": "password123"},
        {"username": "user2", "email": "user2@example.com", "password": "password123"},
        {"username": "user3", "email": "user3@example.com", "password": "password123"},
        {"username": "user4", "email": "user4@example.com", "password": "password123"},
        {"username": "user5", "email": "user5@example.com", "password": "password123"},
    ]

    for user_data in users:
        User.objects.create(
            username=user_data["username"],
            email=user_data["email"],
            password=make_password(user_data["password"]),
            is_superuser=False,
            is_staff=False,
            birthdate='1995-06-15',  # Example birthdate, modify as needed
            user_role_id=user_role,  # Assigning last role found
        )

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('backend', '0003_add_blog_post_type')
    ]

    operations = [
        migrations.RunPython(create_users),
    ]
