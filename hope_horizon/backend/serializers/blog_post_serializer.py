from rest_framework import serializers
from backend.models import BlogPost


class BlogPostserializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["id", "date", "title", "content", "blog_post_type_id", "group_id"]
        extra_kwargs = {
            "title": {"required": True},
            "content": {"required": True},
            "blog_post_type_id": {"required": True}
        }
        read_only_fields = ["id", "date", "group_id"]

class BlogPostListSerializer(serializers.Serializer):
    page_information = serializers.SerializerMethodField()
    blog_posts = BlogPostserializer(many=True)

    def get_page_information(self, obj):
        return {
            "page": obj.get('page', 1),
            "page_size": obj.get('page_size', 10),
            "actualSize": len(obj.get('blog_posts', []))
        }

    class Meta:
        fields = ["page_information", "blog_posts"]
