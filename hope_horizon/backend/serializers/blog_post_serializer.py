from rest_framework import serializers
from backend.models import BlogPost, BlogPostType


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["id", "date", "title", "content", "blog_post_type_id"]
        extra_kwargs = {
            "title": {"required": True},
            "content": {"required": True},
            "blog_post_type_id": {"required": True}
        }
        read_only_fields = ["id", "date"]

class BlogPostListSerializer(serializers.Serializer):
    pageInformation = serializers.SerializerMethodField()
    blog_posts = BlogPostSerializer(many=True)

    def get_pageInformation(self, obj):
        return {
            "page": obj.get('page', 1),
            "pageSize": obj.get('pageSize', 10),
            "actualSize": len(obj.get('blog_posts', []))
        }

    class Meta:
        fields = ["pageInformation", "blog_posts"]
