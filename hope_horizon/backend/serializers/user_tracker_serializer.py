from rest_framework import serializers
from backend.models import UserTracker


class UserTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTracker
        fields = [
            "id",
            "is_enabled",
            "track_mood",
            "track_energy_level",
            "track_sleep_quality",
            "track_anxiety_level",
            "track_appetite",
            "track_content",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "is_enabled": {"required": True},
            "track_mood": {"required": True},
            "track_energy_level": {"required": True},
            "track_sleep_quality": {"required": True},
            "track_anxiety_level": {"required": True},
            "track_appetite": {"required": True},
            "track_content": {"required": True},
        }
