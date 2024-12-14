from rest_framework import serializers
from backend.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'date', 'content', 'user_id', 'blog_post_id']
        read_only_fields = ['id', 'date', 'user_id']
        extra_kwargs = {
            'content': {'required': True},
            'blog_post_id': {'required': True},
        }
