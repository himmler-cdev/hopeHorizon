from django.db import models

class Quote(models.Model):
    quote = models.CharField(max_length=1024)
    author = models.CharField(max_length=1024)
