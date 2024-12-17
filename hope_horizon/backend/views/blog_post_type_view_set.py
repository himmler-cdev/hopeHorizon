from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.serializers import BlogPostTypeSerializer
from rest_framework.permissions import IsAuthenticated
from backend.models import BlogPostType


class BlogPostTypeViewSet(viewsets.ModelViewSet):
    queryset = BlogPostType.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostTypeSerializer

    def list(self, request):
        serializer = BlogPostTypeSerializer(self.queryset, many=True)
        return Response({"blog_post_types": serializer.data}, status=status.HTTP_200_OK)
