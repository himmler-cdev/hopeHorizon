# Generated by Django 4.2.16 on 2024-11-26 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_add_user_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthdate',
            field=models.DateField(null=True),
        ),
    ]