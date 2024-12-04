from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from backend.models import BlogPost, BlogPostType, UserRole
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
        owned = request.GET.get('owned', None)
        workspace = request.GET.get('workspace', None)

        # Pagination
        if page < 1:
            return Response({"detail": "Page must be >= 1"}, status=status.HTTP_400_BAD_REQUEST)
        if pageSize < 1:
            return Response({"detail": "PageSize must be >= 1"}, status=status.HTTP_400_BAD_REQUEST)

        # Filtering
        if blog_post_type_id:
            try:
                BlogPostType.objects.get(id=blog_post_type_id)
            except BlogPostType.DoesNotExist:
                return Response({"detail": "Invalid blog post type id"}, status=status.HTTP_400_BAD_REQUEST)
            blogPosts = BlogPost.objects.filter(title__icontains=search, blog_post_type_id=blog_post_type_id)
        else:
            blogPosts = BlogPost.objects.filter(title__icontains=search)

        # Owned, therapist and workspace filtering
        if workspace is not None and workspace.lower() not in ['true', 'false']:
            return Response({"detail": "Invalid value for workspace parameter"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.user_role_id == UserRole.objects.get(role="Therapist") and workspace is not None and workspace.lower() == 'true':
            protected_blog_post_type = BlogPostType.objects.get(type="Protected")
            public_blog_post_type = BlogPostType.objects.get(type="Public")
            blogPosts = blogPosts.filter(blog_post_type_id__in=[protected_blog_post_type.id, public_blog_post_type.id])
            blogPosts = blogPosts.order_by('-blog_post_type_id', 'date')
        else:
            if owned is not None:
                if owned.lower() == 'true':
                    blogPosts = blogPosts.filter(user_id=request.user.id)
                elif owned.lower() == 'false':
                    public_blog_post_type = BlogPostType.objects.get(type="Public")
                    blogPosts = blogPosts.exclude(user_id=request.user.id).filter(blog_post_type_id=public_blog_post_type.id)
                else:
                    return Response({"detail": "Invalid value for owned parameter"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Owned parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            blogPosts = blogPosts.order_by('-date')

        offset = (page - 1) * pageSize
        blogPosts = blogPosts[offset:offset + pageSize]
        totalPosts = blogPosts.count()

        # TODO: Add group_name filtering and groups in general

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
            blog_post = self.queryset.get(id=pk)
        except BlogPost.DoesNotExist:
            return Response({"detail": "Blog post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # TODO: Check if user is in group of the blog_post
        if (blog_post.user_id == request.user or blog_post.blog_post_type_id == BlogPostType.objects.get(type="Public")):
            serializer = self.serializers["default"](blog_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return Response({"detail": "You are not allowed to view this blog post"}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        serializer = self.serializers["default"](data=request.data)
        if not serializer.is_valid():
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        try: 
            blog_post = self.queryset.get(id=pk)
        except BlogPost.DoesNotExist:
            return Response({"detail": "Blog post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if blog_post.user_id != request.user:
            return Response({"detail": "You are not allowed to update this blog post"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.serializers["default"](blog_post, data=request.data)
        if not serializer.is_valid():
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        try:
            blog_post = self.queryset.get(id=pk)
        except BlogPost.DoesNotExist:
            return Response({"detail": "Blog post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if blog_post.user_id != request.user and request.user.user_role_id != UserRole.objects.get(role="Moderator"):
            return Response({"detail": "You are not allowed to delete this blog post"}, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(blog_post)
        return Response(status=status.HTTP_204_NO_CONTENT)
