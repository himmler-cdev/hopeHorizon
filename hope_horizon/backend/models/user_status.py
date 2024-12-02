from django.db import models
from .user import User


class UserStatus(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    mood = models.IntegerField(null=True)
    energy_level = models.IntegerField(null=True)
    sleep_quality = models.IntegerField(null=True)
    anxiety_level = models.IntegerField(null=True)
    appetite = models.IntegerField(null=True)
    content = models.TextField(null=True)
