from django.db import models
from .user import User
from .forum import Forum

class ForumUser(models.Model):
    is_owner = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    forum_id = models.ForeignKey(Forum, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
