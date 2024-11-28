from rest_framework import serializers
from backend.models import UserStatus


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = [
            "id",
            "date",
            "mood",
            "energy_level",
            "sleep_quality",
            "anxiety_level",
            "appetite",
            "content",
        ]
        read_only_fields = ["id", "date"]
        extra_kwargs = {
            "mood": {"required": True},
            "energy_level": {"required": True},
            "sleep_quality": {"required": True},
            "anxiety_level": {"required": True},
            "appetite": {"required": True},
            "content": {"required": True},
        }
