from django.db import models
from .user import User
from .comment import Comment
from .forum import Forum

class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    comment_id = models.ForeignKey(Comment, null=True, on_delete=models.PROTECT)
    forum_id = models.ForeignKey(Forum, null=True, on_delete=models.PROTECT)