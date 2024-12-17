from django.db import models
from .user import User
from .comment import Comment
from .group import CustomGroup

class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    comment_id = models.ForeignKey(Comment, null=True, on_delete=models.PROTECT)
    group_id = models.ForeignKey(CustomGroup, null=True, on_delete=models.PROTECT)