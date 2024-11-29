from rest_framework import serializers
from backend.models import BlogPostType


class BlogPostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostType
        fields = "__all__"
        read_only_fields = ["id", "type"]
