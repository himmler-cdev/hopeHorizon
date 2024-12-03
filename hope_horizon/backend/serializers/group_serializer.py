from rest_framework import serializers
from backend.models import CustomGroup


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomGroup
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]
