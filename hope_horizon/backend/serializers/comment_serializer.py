from rest_framework import serializers
from backend.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'date', 'content', 'user_id', 'username', 'blog_post_id']
        read_only_fields = ['id', 'date', 'user_id']
        extra_kwargs = {
            'content': {'required': True},
            'blog_post_id': {'required': True},
        }
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['username'] = instance.user_id.username
        return representation
