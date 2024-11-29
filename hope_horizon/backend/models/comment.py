from django.db import models
from .blog_post import BlogPost
from .user import User


class Comment(models.Model):
    content = models.TextField()
    date = models.DateField()
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    