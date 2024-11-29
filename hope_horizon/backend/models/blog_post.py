from django.db import models
from .blog_post_type import BlogPostType
from .user import User


class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    date = models.DateField()
    content = models.TextField()
    type = models.ForeignKey(BlogPostType, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # TODO: Add Group FK here @Kamilo
