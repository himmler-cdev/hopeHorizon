from rest_framework import serializers
from backend.models import GroupUser


class GroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupUser
        fields = "__all__"
        read_only_fields = ["id"]
