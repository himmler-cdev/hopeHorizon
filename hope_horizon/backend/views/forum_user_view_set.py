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
            forum_user = ForumUser.objects.filter(forum_id=forum, user_id=user).get()
            if not forum_user.is_owner:
                return Response({"detail": "You are not the owner of the forum"}, status=status.HTTP_403_FORBIDDEN)
        except ForumUser.DoesNotExist:
            return Response({"detail": "You are not a member of the forum"}, status=status.HTTP_403_FORBIDDEN)
        
        forum_user_list = ForumUser.objects.filter(forum_id=forum, is_active=True, is_owner=False)

        
        if not forum_user_list.exists():
            serializer = self.serializer_class([forum_user], many=True)  # Owner as a list
        else:
            serializer = self.serializer_class(forum_user_list, many=True)
    
        return Response({"forum_users": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request):
        print("Received Forum User Data:", request.data)
        try:
            forum = Forum.objects.get(pk=request.data.get("forum_id"))
        except Forum.DoesNotExist:
            return Response({"detail": "Forum not found"}, status=status.HTTP_400_BAD_REQUEST)
        if not forum.is_active:
            return Response({"detail": "Forum not found"}, status=status.HTTP_400_BAD_REQUEST)
        if not ForumUser.objects.filter(forum_id=forum, user_id=request.user, is_owner=True).exists():
            return Response({"detail": "You are not authorized to add forum users"}, status=status.HTTP_403_FORBIDDEN)
        
        # check if the users to add, exist, are active and are not already in the forum
        user_ids = request.data.get("users", [])
       
        if not user_ids:
            return Response({"detail": "No users provided"}, status=status.HTTP_400_BAD_REQUEST)
        # create a new forum user for each user
        errors = []
        successfully_added = []

        for new_forum_user_dict in user_ids:
            try:
                new_forum_user_id = new_forum_user_dict.get("user_id")
                print("Received user ID:", new_forum_user_id)
                new_forum_user = User.objects.get(pk=new_forum_user_id)

                if not new_forum_user.is_active:
                    errors.append({"user_id": new_forum_user_id, "detail": "User is inactive"})
                    continue  # Skip this user and continue with others

                if ForumUser.objects.filter(forum_id=forum, user_id=new_forum_user).exists():
                    errors.append({"user_id": new_forum_user_id, "detail": "User already exists in the forum"})
                    continue  # Skip this user and continue with others

                # add the user to the forum
                Notification.objects.create(
                    is_read=False,
                    content=f"You have been invited to forum: {forum.name}",
                    user_id=new_forum_user,  # Notify the blog post owner
                    forum_id=forum
                    )
                ForumUser.objects.create(forum_id=forum, user_id=new_forum_user, is_owner=False, is_active=True)
                successfully_added.append(new_forum_user_id)

            except User.DoesNotExist:
                errors.append({"user_id": new_forum_user_id, "detail": "User not found"})

        # Return response based on success/failure cases
        if not errors:  
            return Response(status=status.HTTP_204_NO_CONTENT)  # No content if all users were added successfully

        return Response(
            {"errors": errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):
        try:
            forum_user = ForumUser.objects.get(pk=pk)
        except ForumUser.DoesNotExist:
            return Response({"detail": "Forum user not found"}, status=status.HTTP_404_NOT_FOUND)
        if not ForumUser.objects.filter(forum_id=forum_user.forum_id, user_id=request.user, is_owner=True).exists():
            return Response({"detail": "You are not authorized to delete this forum user"}, status=status.HTTP_403_FORBIDDEN)
        
        forum_user.is_active = False
        forum_user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)