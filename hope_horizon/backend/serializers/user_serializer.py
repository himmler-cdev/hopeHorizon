from rest_framework import serializers
from backend.models import User, UserRole


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
        read_only_fields = ["id", "username"]


class UserDetailsSerializer(serializers.ModelSerializer):
    user_role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "birthdate", "user_role"]
        read_only_fields = ["id", "username", "email", "birthdate", "user_role"]

    def get_user_role(self, obj):
        return obj.user_role_id.role


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "birthdate"]
        extra_kwargs = {
            "username": {"required": True},
            "password": {"required": True},
            "email": {"required": True},
            "birthdate": {"required": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        if len(value) == 0:
            raise serializers.ValidationError("Email cannot be empty")
        return value
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "birthdate"]
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
            "birthdate": {"required": True},
        }