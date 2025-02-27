from django.db import migrations

def add_blog_post_type(apps, schema_editor):
    BlogPostType = apps.get_model('backend', 'BlogPostType')
    BlogPostType.objects.create(type='Public')
    BlogPostType.objects.create(type='Protected')
    BlogPostType.objects.create(type='Private')
    BlogPostType.objects.create(type='Forum')


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('backend', '0002_add_user_roles')
    ]

    operations = [
        migrations.RunPython(add_blog_post_type),
    ]
