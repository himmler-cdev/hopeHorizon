from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.serializers import GroupUserSerializer
from backend.models import CustomGroup, GroupUser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class GroupUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class_group_user = GroupUserSerializer

    def list(self, request):
        user = request.user
        id = request.query_params.get("group_id", None)
        try:
            group = CustomGroup.objects.get(pk=id)
        except CustomGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not group.is_active:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            group_user = GroupUser.objects.filter(group=group).filter(user=user).get()
            if not group_user.is_owner:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except GroupUser.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        group_user_list = GroupUser.objects.filter(group=group).filter(is_active=True).filter(is_owner=False)
        serializer = self.serializer_class_group_user(group_user_list, many=True)
        return Response({"group_users": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, pk=None):
        #TODO: Notifications
        pass

    def destroy(self, request, pk=None):
        group_user = GroupUser.objects.get(pk=pk)
        group_user.is_active = False
        group_user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)