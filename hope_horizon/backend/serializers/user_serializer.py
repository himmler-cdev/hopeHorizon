from rest_framework import serializers
from backend.models import User, UserRole


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
        read_only_fields = ["id", "username"]


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "birthdate", "user_role_id"]
        read_only_fields = ["id", "username", "email", "birthdate", "user_role_id"]


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "birthdate", "user_role_id"]
        extra_kwargs = {
            "username": {"required": True},
            "password": {"required": True},
            "email": {"required": True},
            "birthdate": {"required": True},
            "user_role_id": {"required": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        if len(value) == 0:
            raise serializers.ValidationError("Email cannot be empty")
        return value