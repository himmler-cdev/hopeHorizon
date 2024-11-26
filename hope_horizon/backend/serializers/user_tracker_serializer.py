from rest_framework import serializers
from backend.models import UserTracker


class UserTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTracker
        fields = "__all__"
        read_only_fields = ["id"]
