from rest_framework import serializers
from backend.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)
    blog_post_id = serializers.IntegerField(source='blog_post_id.id', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'date', 'content', 'username', 'blog_post_id']
        read_only_fields = ['id', 'date', 'username', 'blog_post_id']
        extra_kwargs = {
            'content': {'required': True},
            'username': {'required': True},
            'blog;_post_id': {'required': True},
            'date': {'required': True}
        }
