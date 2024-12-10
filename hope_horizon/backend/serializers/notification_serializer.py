from rest_framework import serializers
from backend.models import Notification

# Notification Serializer: For full details of a notification
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "content", "is_read", "created_at", "user_id"] #TODO comment_id, group_id
        extra_kwargs = {
            "content": {"required": True},
        }
        read_only_fields = ["id", "created_at", "user_id"] #TODO comment_id, group_id