from django.contrib.auth.models import AbstractUser
from django.db import models
from .user_tracker import UserTracker
from .user_role import UserRole

class User(AbstractUser):
    user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True)
    user_tracker = models.OneToOneField(UserTracker, on_delete=models.CASCADE, null=True)