from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.serializers import GroupSerializer
from backend.models import CustomGroup, GroupUser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer

    def list(self, request):
        user = request.user
        owned = request.query_params.get('owned', None)
        if owned is None:
            return Response({"detail": "Parameter owned is missing"}, status=status.HTTP_400_BAD_REQUEST)
        if owned.lower() == "true":
            group_user_owned = GroupUser.objects.filter(user_id=user, is_owner=True, is_active=True)
            groups = CustomGroup.objects.filter(id__in=group_user_owned.values_list("group_id", flat=True))
        else:
            group_user_member = GroupUser.objects.filter(user_id=user, is_owner=False, is_active=True)
            groups = CustomGroup.objects.filter(id__in=group_user_member.values_list("group_id", flat=True))
        serializer = self.serializer_class(groups, many=True)
        return Response({"custom_groups": serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = request.user
        try:
            group = CustomGroup.objects.get(pk=pk)
        except CustomGroup.DoesNotExist:
            return Response({"detail": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        if not group.is_active:
            return Response({"detail": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        if not GroupUser.objects.filter(group_id=group, user_id=user, is_active=True, is_owner=True).exists():
            return Response({"detail": "User not authorized"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        name = request.data.get("name")
        description = request.data.get("description")
        serializer = GroupSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        group = CustomGroup.objects.create(name=name, description=description)
        GroupUser.objects.create(user_id=request.user, group_id=group, is_owner=True, is_active=True)
        serializer = self.get_serializer(group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = request.user
        serializer = GroupSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            group = CustomGroup.objects.get(pk=pk)
        except CustomGroup.DoesNotExist:
            return Response({"detail": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        if not group.is_active:
            return Response({"detail": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        group_user = GroupUser.objects.filter(user_id=user, group_id=group, is_active=True, is_owner=True)
        if not group_user.exists():
            return Response({"detail": "User not authorized"}, status=status.HTTP_403_FORBIDDEN)
        
        group.name = request.data.get("name")
        group.description = request.data.get("description")
        group.save()
        serializer = self.get_serializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        user = request.user
        try:
            group = CustomGroup.objects.get(pk=pk)
        except CustomGroup.DoesNotExist:
            return Response({"detail": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        if not group.is_active:
            return Response({"detail": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        group_user = GroupUser.objects.filter(user_id=user, group_id=group, is_active=True, is_owner=True)
        if not group_user.exists():
            return Response({"detail": "User not authorized"}, status=status.HTTP_403_FORBIDDEN)
        group.is_active = False
        group.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
