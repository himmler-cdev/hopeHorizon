from rest_framework import serializers
from backend.models import UserStatus


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = "__all__"
        read_only_fields = ["id"]
