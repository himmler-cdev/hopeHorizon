from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from backend.models import BlogPost, BlogPostType, UserRole, GroupUser, CustomGroup
from backend.serializers import blog_postserializer, BlogPostListSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializers = {
        "default": blog_postserializer,
        "list": BlogPostListSerializer
    }
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Query parameters
        try: 
            page = request.GET.get('page', None)
            page_size = int(request.GET.get('page_size', 10))
            if page is None:
                return Response({"detail": "Page parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            page = int(page)
        except ValueError:
            return Response({"detail": "page_size must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
                       
        search = request.GET.get('search', '')
        blog_post_type_id = request.GET.get('blog_post_type_id', None)
        owned = request.GET.get('owned', None)
        workspace = request.GET.get('workspace', None)
        group_name = request.GET.get('group_name', None)

        # Pagination
        if page < 1:
            return Response({"detail": "Page must be >= 1"}, status=status.HTTP_400_BAD_REQUEST)
        if page_size < 1:
            return Response({"detail": "page_size must be >= 1"}, status=status.HTTP_400_BAD_REQUEST)

        # Filtering
        if blog_post_type_id:
            try:
                blog_post_type_id = int(blog_post_type_id)
                BlogPostType.objects.get(id=blog_post_type_id)
            except ValueError:
                return Response({"detail": "Invalid blog post type id"}, status=status.HTTP_400_BAD_REQUEST)
            except BlogPostType.DoesNotExist:
                return Response({"detail": "Invalid blog post type id"}, status=status.HTTP_400_BAD_REQUEST)
            blog_posts = BlogPost.objects.filter(title__icontains=search, blog_post_type_id=blog_post_type_id)
        else:
            blog_posts = BlogPost.objects.filter(title__icontains=search)

        # Owned, therapist and workspace filtering
        if workspace is not None and workspace.lower() not in ['true', 'false']:
            return Response({"detail": "Invalid value for workspace parameter"}, status=status.HTTP_400_BAD_REQUEST)

        # Group filtering
        if blog_post_type_id == BlogPostType.objects.get(type="Group").id:
            if group_name is not None:
                group = CustomGroup.objects.filter(name__icontains=group_name).first()
                if group and GroupUser.objects.filter(group_id=group.id, user_id=request.user.id, is_active=True).exists():
                    blog_posts = blog_posts.filter(group_id=group.id)
                else:
                    return Response({"detail": "You are not a member of the requested group or the group does not exist"}, status=status.HTTP_403_FORBIDDEN)
            else:
                group_ids = GroupUser.objects.filter(user_id=request.user.id, is_active=True).values_list('group_id', flat=True)
                blog_posts = blog_posts.filter(group_id__in=group_ids)
        # Check if user is a therapist
        elif request.user.user_role_id == UserRole.objects.get(role="Therapist"):
            blog_posts = self._filter_for_therapist(blog_posts, workspace)
        # Check if user is not a therapist and owned parameter is provided
        else: 
            if owned is not None:
                if owned.lower() == 'true':
                    blog_posts = blog_posts.filter(user_id=request.user.id)
                elif owned.lower() == 'false':
                    public_blog_post_type = BlogPostType.objects.get(type="Public")
                    blog_posts = blog_posts.exclude(user_id=request.user.id).filter(blog_post_type_id=public_blog_post_type.id)
                else:
                    return Response({"detail": "Invalid value for owned parameter"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Owned parameter is required for non-therapist users"}, status=status.HTTP_400_BAD_REQUEST)
            blog_posts = blog_posts.order_by('-date')
        
        offset = (page - 1) * page_size
        blog_posts = blog_posts[offset:offset + page_size]
        totalPosts = blog_posts.count()

        data = {
            "page": page,
            "page_size": page_size,
            "actualSize": totalPosts,
            "blog_posts": blog_posts
        }

        serializer = self.serializers["list"](data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        try:
            blog_post = self.queryset.get(id=pk)
        except BlogPost.DoesNotExist:
            return Response({"detail": "Blog post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Checks if user is the owner of the blog_post or if the blog_post is public
        if blog_post.user_id == request.user or blog_post.blog_post_type_id == BlogPostType.objects.get(type="Public"):
            serializer = self.serializers["default"](blog_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Checks if the user is a therapist and the blog_post is protected
        if request.user.user_role_id == UserRole.objects.get(role="Therapist") and blog_post.blog_post_type_id == BlogPostType.objects.get(type="Protected"):
            serializer = self.serializers["default"](blog_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Check if user is in group of the blog_post
        group_users = GroupUser.objects.filter(group_id=blog_post.group_id, user_id=request.user.id, is_active=True)
        if blog_post.blog_post_type_id == BlogPostType.objects.get(type="Group") and group_users.exists():
            serializer = self.serializers["default"](blog_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return Response({"detail": "You are not allowed to view this blog post"}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        serializer = self.serializers["default"](data=request.data)
        if not serializer.is_valid():
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user tries to create a group blog post
        if request.data.get('blog_post_type_id', None) == BlogPostType.objects.get(type="Group").id:
            try:
                CustomGroup.objects.get(id=request.data.get('group_id'))
            except CustomGroup.DoesNotExist:
                return Response({"detail": "Invalid group id"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user_id=request.user, group_id_id=request.data.get('group_id'))
        else:
            serializer.save(user_id=request.user, group_id=None)

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
        
        # Check if user tries to create a group blog post
        if request.data.get('blog_post_type_id', None) == BlogPostType.objects.get(type="Group").id:
            try:
                CustomGroup.objects.get(id=request.data.get('group_id'))
            except CustomGroup.DoesNotExist:
                return Response({"detail": "Invalid group id"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(group_id_id=request.data.get('group_id'))
        else:
            serializer.save(group_id=None)

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

    # Helper functions for list
    def _filter_for_therapist(self, blog_posts, workspace):
        if workspace is not None and workspace.lower() == 'true':
            protected_blog_post_type = BlogPostType.objects.get(type="Protected")
            public_blog_post_type = BlogPostType.objects.get(type="Public")
            blog_posts = blog_posts.filter(blog_post_type_id__in=[protected_blog_post_type.id, public_blog_post_type.id])
            blog_posts = blog_posts.order_by('-blog_post_type_id', 'date')
        else:
            public_blog_post_type = BlogPostType.objects.get(type="Public")
            blog_posts = blog_posts.filter(blog_post_type_id=public_blog_post_type.id)

        return blog_posts
