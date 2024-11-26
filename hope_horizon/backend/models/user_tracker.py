from django.db import models


class UserTracker(models.Model):
    is_enabled = models.BooleanField(default=False)
    track_mood = models.BooleanField(default=False)
    track_energy_level = models.BooleanField(default=False)
    track_sleep_quality = models.BooleanField(default=False)
    track_anxiety_level = models.BooleanField(default=False)
    track_appetite = models.BooleanField(default=False)
    track_content = models.BooleanField(default=False)
