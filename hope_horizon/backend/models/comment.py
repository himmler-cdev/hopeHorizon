from django.db import models
from .blog_post import BlogPost
from .user import User


class Comment(models.Model):
    content = models.TextField(max_length=500)
    date = models.DateField(auto_now_add=True)
    blog_post_id = models.ForeignKey(BlogPost, on_delete=models.PROTECT, null=True)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    