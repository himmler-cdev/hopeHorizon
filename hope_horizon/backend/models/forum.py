from django.db import models

class Forum(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
