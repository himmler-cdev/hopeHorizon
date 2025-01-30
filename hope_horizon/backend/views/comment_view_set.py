from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.paginator import Paginator
from backend.models import Comment
from backend.models import BlogPost
from backend.models import Notification
from backend.serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def list(self, request):
        blog_id = request.query_params.get('blog')
        page = int(request.query_params.get('page', 0))

        if not blog_id:
            return Response({"detail": "Blog ID required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            blog_id = int(blog_id)  # Ensure the ID is a valid integer
        except (ValueError, TypeError):
            return Response({"detail": "Invalid blog ID format"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            blog_post = BlogPost.objects.get(id=blog_id)
        except BlogPost.DoesNotExist:
            return Response({"detail": "Blog post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if blog_post.blog_post_type_id.type == "Protected" and (blog_post.user_id != request.user and (request.user.user_role_id.role != "Therapist" and request.user.user_role_id.role != "Moderator")
            ):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        if blog_post.blog_post_type_id.type == "Private" and blog_post.user_id != request.user and request.user.user_role_id.role != "Moderator":
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        comments = blog_post.comment_set.all().order_by('-date')
        paginator = Paginator(comments, 10)
                
        page_obj = paginator.get_page(page + 1)
        serializer = CommentSerializer(page_obj.object_list, many=True)

        return Response({
            "pageInformation": {
                "page": page,
                "page_size": 10,
                "actual_size": page_obj.paginator.count
            },
            "comments": serializer.data
        })


    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"detail": "Invalid ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        if (
            (comment.blog_post_id.blog_post_type_id.type == "Protected" and (comment.blog_post_id.user_id != request.user and (request.user.user_role_id.role != "Therapist" and request.user.user_role_id.role != "Moderator"))) or
            (comment.blog_post_id.blog_post_type_id.type == "Private" and (comment.blog_post_id.user_id != request.user and request.user.user_role_id.role != "Moderator"))
                ):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        blog_post_id = request.data.get('blog_post_id')

        if not serializer.is_valid():
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        blog_post = BlogPost.objects.get(id=blog_post_id)
        
        if (
            (blog_post.blog_post_type_id.type == "Protected" and (blog_post.user_id != request.user and request.user.user_role_id.role != "Therapist")) or
            (blog_post.blog_post_type_id.type == "Private" and blog_post.user_id != request.user)
                ):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        comment = serializer.save(user_id=request.user)

        Notification.objects.create(
            is_read=False,
            content=f"A new comment was added to your blog post: {blog_post.title}",
            user_id=blog_post.user_id,  # Notify the blog post owner
            comment_id=comment,  # Reference the created comment
            forum_id=blog_post.forum_id if hasattr(blog_post, 'forum_id') else None  # Optional forum association
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            pk = int(pk)
        except ValueError:
            return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if 'content' not in request.data or not request.data.get('content', '').strip():
            return Response({"detail": "Content field is required and cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        if comment.user_id != request.user and not request.user.user_role_id.role == "Moderator":
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        comment.content = request.data.get("content")
        comment.save()
        return Response({"content": comment.content},status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"detail": "Invalid ID"}, status=status.HTTP_400_BAD_REQUEST)
       
        if comment.user_id != request.user and not request.user.user_role_id.role == "Moderator":
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
