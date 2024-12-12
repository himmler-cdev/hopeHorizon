from django.db import models
from .blog_post import BlogPost
from .user import User


class Comment(models.Model):
    content = models.TextField()
    date = models.DateField() #TODO: autogenerate?
    blog_post_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    