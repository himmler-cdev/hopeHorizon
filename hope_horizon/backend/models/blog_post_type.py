from django.db import models


class BlogPostType(models.Model):
    type = models.CharField(max_length=50, default="Private")
