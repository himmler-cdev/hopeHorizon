from django.db import models
from backend.models.user import User
from backend.models.group import CustomGroup

class GroupUser(models.Model):
    is_owner = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    group_id = models.ForeignKey(CustomGroup, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
