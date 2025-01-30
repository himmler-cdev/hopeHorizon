from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.serializers import ForumSerializer
from backend.models import Forum, ForumUser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class ForumViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ForumSerializer

    def list(self, request):
        user = request.user
        owned = request.query_params.get('owned', None)
        if owned is None:
            return Response({"detail": "Parameter owned is missing"}, status=status.HTTP_400_BAD_REQUEST)
        if owned.lower() == "true":
            forum_user_owned = ForumUser.objects.filter(user_id=user, is_owner=True, is_active=True)
            forums = Forum.objects.filter(id__in=forum_user_owned.values_list("forum_id", flat=True))
        else:
            forum_user_member = ForumUser.objects.filter(user_id=user, is_owner=False, is_active=True)
            forums = Forum.objects.filter(id__in=forum_user_member.values_list("forum_id", flat=True))
        serializer = self.serializer_class(forums, many=True)
        return Response({"custom_forums": serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = request.user
        try:
            forum = Forum.objects.get(pk=pk)
        except Forum.DoesNotExist:
            return Response({"detail": "Forum not found"}, status=status.HTTP_404_NOT_FOUND)
        if not forum.is_active:
            return Response({"detail": "Forum not found"}, status=status.HTTP_404_NOT_FOUND)
        if not ForumUser.objects.filter(forum_id=forum, user_id=user, is_active=True, is_owner=True).exists():
            return Response({"detail": "User not authorized"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(forum)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        name = request.data.get("name")
        description = request.data.get("description")
        serializer = ForumSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        forum = Forum.objects.create(name=name, description=description)
        ForumUser.objects.create(user_id=request.user, forum_id=forum, is_owner=True, is_active=True)
        serializer = self.get_serializer(forum)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        user = request.user
        try:
            forum = Forum.objects.get(pk=pk)
        except Forum.DoesNotExist:
            return Response({"detail": "Forum not found"}, status=status.HTTP_404_NOT_FOUND)

        if not forum.is_active:
            return Response({"detail": "Forum not found"}, status=status.HTTP_404_NOT_FOUND)

        forum_user = ForumUser.objects.filter(user_id=user, forum_id=forum, is_active=True, is_owner=True)
        if not forum_user.exists():
            return Response({"detail": "User not authorized"}, status=status.HTTP_403_FORBIDDEN)


        serializer = ForumSerializer(instance=forum, data=request.data, partial=True)
        
        forum = serializer.save()  # ✅ Use `serializer.save()` to update safely
        return Response(serializer.data, status=status.HTTP_200_OK)


#    def update(self, request, pk=None):
#        user = request.user
#
#        if not serializer.is_valid():
#            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#        try:
#            forum = Forum.objects.get(pk=pk)
#        except Forum.DoesNotExist:
#            return Response({"detail": "Forum not found"}, status=status.HTTP_404_NOT_FOUND)
#        if not forum.is_active:
#            return Response({"detail": "Forum not found"}, status=status.HTTP_404_NOT_FOUND)
#        forum_user = ForumUser.objects.filter(user_id=user, forum_id=forum, is_active=True, is_owner=True)
#        if not forum_user.exists():
#            return Response({"detail": "User not authorized"}, status=status.HTTP_403_FORBIDDEN)
#        
#        forum.name = request.data.get("name")
#        forum.description = request.data.get("description")
#        forum.save()
#        serializer = self.get_serializer(forum)
#        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        user = request.user
        try:
            forum = Forum.objects.get(pk=pk)
        except Forum.DoesNotExist:
            return Response({"detail": "Forum not found"}, status=status.HTTP_404_NOT_FOUND)
        if not forum.is_active:
            return Response({"detail": "Forum not found"}, status=status.HTTP_404_NOT_FOUND)
        forum_user = ForumUser.objects.filter(user_id=user, forum_id=forum, is_active=True, is_owner=True)
        if not forum_user.exists():
            return Response({"detail": "User not authorized"}, status=status.HTTP_403_FORBIDDEN)
        ForumUser.objects.filter(forum_id=forum).update(is_active=False)
        forum.is_active = False
        forum.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
