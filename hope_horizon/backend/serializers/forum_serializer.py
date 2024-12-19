from rest_framework import serializers
from backend.models import Forum


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": True},
        }
