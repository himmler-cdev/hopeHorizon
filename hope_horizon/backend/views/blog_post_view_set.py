from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from backend.models import BlogPost, BlogPostType
from backend.serializers import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        pass

    def retrieve(self, request, pk):
        try:
            blog_post = self.get_object()
        except BlogPost.DoesNotExist:
            return Response({"errors": ["Blog post not found"]}, status=status.HTTP_404_NOT_FOUND)
        
        # TODO: Check if user is in group of the blog_post
        if (blog_post.user_id == request.user or blog_post.blog_post_type_id == BlogPostType.objects.get(type="Public")):
            serializer = self.get_serializer(blog_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return Response({"errors": ["You are not allowed to view this blog post"]}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        pass

    def destroy(self, request, pk):
        blog_post = self.get_object()
        if blog_post.user_id != request.user:
            return Response({"errors": ["You are not allowed to delete this blog post"]}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(blog_post)
        return Response(status=status.HTTP_204_NO_CONTENT)
