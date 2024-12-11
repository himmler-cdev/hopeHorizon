from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.serializers import GroupUserSerializer
from backend.models import CustomGroup, GroupUser, User
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class GroupUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupUserSerializer

    def list(self, request):
        user = request.user
        id = request.query_params.get("group_id", None)
        try:
            group = CustomGroup.objects.get(pk=id)
        except CustomGroup.DoesNotExist:
            return Response({"detail": "The group does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if not group.is_active:
            return Response({"detail": "The group does not exist"}, status=status.HTTP_404_NOT_FOUND)
        try:
            group_user = GroupUser.objects.filter(group_id=group, user_id=user).get()
            if not group_user.is_owner:
                return Response({"detail": "You are not the owner of the group"}, status=status.HTTP_403_FORBIDDEN)
        except GroupUser.DoesNotExist:
            return Response({"detail": "You are not a member of the group"}, status=status.HTTP_403_FORBIDDEN)
        
        group_user_list = GroupUser.objects.filter(group_id=group, is_active=True, is_owner=False)
        serializer = self.serializer_class(group_user_list, many=True)
        return Response({"group_users": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            group = CustomGroup.objects.get(pk=request.data.get("group_id"))
        except CustomGroup.DoesNotExist:
            return Response({"detail": "Group not found"}, status=status.HTTP_400_BAD_REQUEST)
        if not group.is_active:
            return Response({"detail": "Group not found"}, status=status.HTTP_400_BAD_REQUEST)
        if not GroupUser.objects.filter(group_id=group, user_id=request.user, is_owner=True).exists():
            return Response({"detail": "You are not authorized to add group users"}, status=status.HTTP_403_FORBIDDEN)
        
        # check if the users to add, exist, are active and are not already in the group
        user_ids = request.data.get("users", [])
        if not user_ids:
            return Response({"detail": "No users provided"}, status=status.HTTP_400_BAD_REQUEST)
        # create a new group user for each user
        for new_group_user_id in user_ids:
            new_group_user = User.objects.get(pk=new_group_user_id)
            if not new_group_user.is_active:
                return Response({"detail": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
            if GroupUser.objects.filter(group_id=group, user_id=new_group_user).exists():
                return Response({"detail": "User already exists in the group"}, status=status.HTTP_400_BAD_REQUEST)
            # add the user to the group
            GroupUser.objects.create(group_id=group, user_id=new_group_user, is_owner=False, is_active=True)

        #TODO: Notifications
        return Response({"detail": "User(s) added successfully"}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            group_user = GroupUser.objects.get(pk=pk)
        except GroupUser.DoesNotExist:
            return Response({"detail": "Group user not found"}, status=status.HTTP_404_NOT_FOUND)
        if not GroupUser.objects.filter(group_id=group_user.group_id, user_id=request.user, is_owner=True).exists():
            return Response({"detail": "You are not authorized to delete this group user"}, status=status.HTTP_403_FORBIDDEN)
        
        group_user.is_active = False
        group_user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)