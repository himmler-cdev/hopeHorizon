from django.db import models
from .user import User


class UserTracker(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.PROTECT)
    is_enabled = models.BooleanField(default=None)
    track_mood = models.BooleanField(default=None)
    track_energy_level = models.BooleanField(default=None)
    track_sleep_quality = models.BooleanField(default=None)
    track_anxiety_level = models.BooleanField(default=None)
    track_appetite = models.BooleanField(default=None)
    track_content = models.BooleanField(default=None)
