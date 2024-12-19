from rest_framework import serializers
from backend.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'is_read', 'date', 'content', 'user_id', 'comment_id', 'forum_id']
        read_only_fields = ['id', 'date']
        extra_kwargs = {
            'content': {'required': True},
            'user_id': {'required': True},
            'comment_id': {'required': True},
        }