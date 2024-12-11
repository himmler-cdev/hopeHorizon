from rest_framework import serializers
from backend.models import GroupUser
from .user_serializer import UserListSerializer

class GroupUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)
    class Meta:
        model = GroupUser
        fields = ["id", "user_id", "username"]
        read_only_fields = ["id"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['username'] = instance.user_id.username
        return representation
