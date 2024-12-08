from django.db import models
from backend.models.user import User
from backend.models.group import CustomGroup

class GroupUser(models.Model):
    is_owner = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE, related_name="group_users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_users")

    class Meta:
        unique_together = ('group', 'user')  # A user can only be in a group once

    def __str__(self):
        return f"{self.user} in {self.group}"