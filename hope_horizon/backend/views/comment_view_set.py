import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.paginator import Paginator
from backend.models import Comment
from backend.models import BlogPost
from backend.serializers import CommentSerializer

class CommentViewSet(viewsets.ViewSet):
    def list(self, request):
        blog_id = request.query_params.get('blog')
        page = int(request.query_params.get('page', 0))

        if not blog_id:
            return Response({"error": "Blog ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            blog_post = BlogPost.objects.get(id=blog_id)
        except BlogPost.DoesNotExist:
            return Response({"error": "Blog post not found"}, status=status.HTTP_404_NOT_FOUND)

        comments = blog_post.comment_set.all().order_by('-date')
        paginator = Paginator(comments, 10)
        if page >= paginator.num_pages:
            return Response({
                "pageInformation": {
                    "page": page,
                    "pageSize": 10,
                    "actualSize": 0
                },
                "comments": []
            }, status=status.HTTP_200_OK)

        page_obj = paginator.get_page(page + 1)
        serializer = CommentSerializer(page_obj.object_list, many=True)

        return Response({
            "pageInformation": {
                "page": page,
                "pageSize": 10,
                "actualSize": page_obj.paginator.count
            },
            "comments": serializer.data
        })

    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def create(self, request):
        blog_post_id = request.data.get('blog_post_id')
        content = request.data.get('content')

        if not blog_post_id or not content:
            return Response({"error": "Both blog_post_id and content are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            blog_post = BlogPost.objects.get(id=blog_post_id)
        except BlogPost.DoesNotExist:
            return Response({"error": "Blog post not found"}, status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.create(
            blog_post_id=blog_post,
            user_id=request.user,
            content=content,
            date=datetime.date.today()
        )

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            pk_int = int(pk)
        except ValueError:
            return Response({"error": "ID parameter must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        # Darf moderator updaten?
        if comment.user_id != request.user and not request.user.user_role_id.role == "Moderator":
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        content = request.data.get('content')
        if not content:
            return Response({"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)

        comment.content = content
        comment.save()

        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
     # Check if the 'pk' is a valid integer
        try:
            pk_int = int(pk)
        except ValueError:
            return Response({"error": "ID parameter must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is the owner of the comment or a Moderator
        if comment.user_id != request.user and not request.user.user_role_id.role == "Moderator":
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        # Delete the comment
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
