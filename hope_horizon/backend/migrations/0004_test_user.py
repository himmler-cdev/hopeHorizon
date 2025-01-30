from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_users_and_blog_posts(apps, schema_editor):
    User = apps.get_model('backend', 'User')
    UserRole = apps.get_model('backend', 'UserRole')
    BlogPost = apps.get_model('backend', 'BlogPost')
    BlogPostType = apps.get_model('backend', 'BlogPostType')

    # Ensure at least one user role exists
    admin_role = UserRole.objects.last()
    user_role = UserRole.objects.first()

    # Create an admin user
    admin = User.objects.create(
        username='admin',
        email='admin@example.com',
        password=make_password('topsecret'),
        is_superuser=True,
        is_staff=True,
        birthdate='2000-01-01',
        user_role_id=admin_role,
    )

    # Create regular users
    users = []
    user_data_list = [
        {"username": "user1", "email": "user1@example.com", "password": "password123"},
        {"username": "user2", "email": "user2@example.com", "password": "password123"},
        {"username": "user3", "email": "user3@example.com", "password": "password123"},
        {"username": "user4", "email": "user4@example.com", "password": "password123"},
        {"username": "user5", "email": "user5@example.com", "password": "password123"},
    ]

    for user_data in user_data_list:
        user = User.objects.create(
            username=user_data["username"],
            email=user_data["email"],
            password=make_password(user_data["password"]),
            is_superuser=False,
            is_staff=False,
            birthdate='1995-06-15',
            user_role_id=user_role,
        )
        users.append(user)

    # Ensure at least one BlogPost exists
    if not BlogPost.objects.exists():
        BlogPost.objects.create(
            title="Dummy Blog Post",
            content="This is a test blog post.",
            blog_post_type_id_id=1,
            user_id=admin,
        )

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('backend', '0003_add_blog_post_type')  # Ensure this migration exists
    ]

    operations = [
        migrations.RunPython(create_users_and_blog_posts),
    ]
