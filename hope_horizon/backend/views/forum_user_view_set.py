import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.models.notification import Notification
from backend.serializers import ForumUserSerializer
from backend.models import Forum, ForumUser, User
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class ForumUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ForumUserSerializer

    def list(self, request):
        user = request.user
        id = request.query_params.get("forum_id", None)
        try:
            forum = Forum.objects.get(pk=id)
        except Forum.DoesNotExist:
            return Response({"detail": "The forum does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if not forum.is_active:
            return Response({"detail": "The forum does not exist"}, status=status.HTTP_404_NOT_FOUND)
        try:
            forum_user = ForumUser.objects.filter(forum_id=forum, user_id=user, is_active=True).get()
            if not forum_user.is_owner:
                serializer = self.serializer_class([forum_user], many=True)
                return Response({"forum_users": serializer.data}, status=status.HTTP_200_OK)
        except ForumUser.DoesNotExist:
            return Response({"detail": "You are not a member of the forum"}, status=status.HTTP_403_FORBIDDEN)
        
        forum_user_list = ForumUser.objects.filter(forum_id=forum, is_active=True)

        if not forum_user_list.exists():
            serializer = self.serializer_class([forum_user], many=True)  # Owner as a list
        else:
            serializer = self.serializer_class(forum_user_list, many=True)
    
        return Response({"forum_users": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request):
        user = request.user
        forum_id = request.data.get("forum_id")
        user_ids = request.data.get("users", [])

        try:
            forum = Forum.objects.get(pk=forum_id)
        except Forum.DoesNotExist:
            return Response({"detail": "Forum not found"}, status=status.HTTP_404_NOT_FOUND)

        if not forum.is_active:
            return Response({"detail": "Forum not found"}, status=status.HTTP_400_BAD_REQUEST)

        if not ForumUser.objects.filter(forum_id=forum, user_id=user, is_owner=True).exists():
            return Response({"detail": "You are not authorized to add forum users"}, status=status.HTTP_403_FORBIDDEN)

        if not user_ids:
            return Response({"detail": "No users provided"}, status=status.HTTP_400_BAD_REQUEST)

        errors = []
        successfully_added = []

        for new_forum_user_id in user_ids:
            try: 
                #user_id = json.loads(new_forum_user_id)
                new_forum_user = User.objects.get(pk=new_forum_user_id)

                if not new_forum_user.is_active:
                    errors.append({"user_id": new_forum_user_id, "detail": "User is inactive"})
                    continue

                existing_forum_user = ForumUser.objects.filter(forum_id=forum, user_id=new_forum_user).first()

                if existing_forum_user:
                    if existing_forum_user.is_active:
                        errors.append({"user_id": new_forum_user_id, "detail": "User already exists in the forum"})
                    else:
                        existing_forum_user.is_active = True
                        existing_forum_user.save()
                        successfully_added.append(new_forum_user_id)
                else:
                    Notification.objects.create(
                        is_read=False,
                        content=f"You have been invited to forum: {forum.name}",
                        user_id=new_forum_user,
                        forum_id=forum
                    )
                    ForumUser.objects.create(forum_id=forum, user_id=new_forum_user, is_owner=False, is_active=True)
                    successfully_added.append(new_forum_user_id)

            except User.DoesNotExist:
                errors.append({"user_id": new_forum_user_id, "detail": "User not found"})

        if not errors:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            forum_user = ForumUser.objects.get(pk=pk)
        except ForumUser.DoesNotExist:
            return Response({"detail": "Forum user not found"}, status=status.HTTP_404_NOT_FOUND)
        if not ForumUser.objects.filter(forum_id=forum_user.forum_id, user_id=request.user).exists():
            return Response({"detail": "You are not authorized to delete this forum user"}, status=status.HTTP_403_FORBIDDEN)
        
        forum_user.is_active = False
        forum_user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)