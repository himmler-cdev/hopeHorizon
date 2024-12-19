from django.db import models
from .blog_post_type import BlogPostType
from .user import User
from .forum import Forum


class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    blog_post_type_id = models.ForeignKey(BlogPostType, on_delete=models.PROTECT, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    forum_id = models.ForeignKey(Forum, on_delete=models.CASCADE, null=True)
