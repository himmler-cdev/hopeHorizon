from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from backend.models import BlogPost, BlogPostType
from backend.serializers import BlogPostSerializer, BlogPostListSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializers = {
        "default": BlogPostSerializer,
        "list": BlogPostListSerializer
    }
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Query parameters
        page = int(request.GET.get('page', 1))
        pageSize = int(request.GET.get('pageSize', 10))
        search = request.GET.get('search', '')
        blog_post_type_id = request.GET.get('blog_post_type_id', None)
        owned = request.GET.get('owned', "true")

        # Pagination
        if page < 1:
            return Response({"errors": ["Page must be >= 1"]}, status=status.HTTP_400_BAD_REQUEST)
        if pageSize < 1:
            return Response({"errors": ["PageSize must be >= 1"]}, status=status.HTTP_400_BAD_REQUEST)

        # Filtering
        if blog_post_type_id:
            try:
                BlogPostType.objects.get(id=blog_post_type_id)
            except BlogPostType.DoesNotExist:
                return Response({"errors": ["Invalid blog post type id"]}, status=status.HTTP_400_BAD_REQUEST)
            blogPosts = BlogPost.objects.filter(title__icontains=search, blog_post_type_id=blog_post_type_id)
        else:
            blogPosts = BlogPost.objects.filter(title__icontains=search)

        # Owned filtering   
        if owned is not None:
            if owned.lower() == 'true':
                blogPosts = blogPosts.filter(user_id=request.user.id)
            elif owned.lower() == 'false':
                public_blog_post_type = BlogPostType.objects.get(type="Public")
                blogPosts = blogPosts.exclude(user_id=request.user.id).filter(blog_post_type_id=public_blog_post_type.id)
            else:
                return Response({"errors": ["Invalid value for owned parameter"]}, status=status.HTTP_400_BAD_REQUEST)

        offset = (page - 1) * pageSize
        blogPosts = blogPosts[offset:offset + pageSize]
        totalPosts = blogPosts.count()

        # TODO: Add group_name filtering and groups in general
        # TODO: Add worspace filtering for therapist (only on commentend blog posts)

        data = {
            "page": page,
            "pageSize": pageSize,
            "actualSize": totalPosts,
            "blog_posts": blogPosts
        }

        serializer = self.serializers["list"](data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        try:
            blog_post = self.get_object()
        except BlogPost.DoesNotExist:
            return Response({"errors": ["Blog post not found"]}, status=status.HTTP_404_NOT_FOUND)
        
        # TODO: Check if user is in group of the blog_post
        if (blog_post.user_id == request.user or blog_post.blog_post_type_id == BlogPostType.objects.get(type="Public")):
            serializer = self.serializers["default"](blog_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return Response({"errors": ["You are not allowed to view this blog post"]}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        serializer = self.serializers["default"](data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        try: 
            blog_post = self.get_object()
        except BlogPost.DoesNotExist:
            return Response({"errors": ["Blog post not found"]}, status=status.HTTP_404_NOT_FOUND)
        
        if blog_post.user_id != request.user:
            return Response({"errors": ["You are not allowed to update this blog post"]}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.serializers["default"](blog_post, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # TODO: Add role based permissions for delete when post is public
    def destroy(self, request, pk):
        blog_post = self.get_object()
        if blog_post.user_id != request.user:
            return Response({"errors": ["You are not allowed to delete this blog post"]}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(blog_post)
        return Response(status=status.HTTP_204_NO_CONTENT)
