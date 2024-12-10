from django.contrib.auth.models import AbstractUser
from django.db import models
from .user_role import UserRole


class User(AbstractUser):
    user_role_id = models.ForeignKey(UserRole, on_delete=models.PROTECT)
    birthdate = models.DateField()
    