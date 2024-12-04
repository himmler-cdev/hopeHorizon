from rest_framework import serializers
from backend.models import GroupUser
from .user_serializer import UserListSerializer

class GroupUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = GroupUser
        fields = ["id", "user_id", "username"]
        read_only_fields = ["id"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_id'] = instance.user.id
        representation['username'] = instance.user.username
        return representation
