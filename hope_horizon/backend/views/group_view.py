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
        owned = request.query_params.get("owned", None)
        if owned is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if owned.lower() == "true":
            group_user_owned = GroupUser.objects.filter(user=user).filter(is_owner=True).filter(is_active=True)
            group = CustomGroup.objects.filter(id__in=group_user_owned.values_list("group", flat=True))
        else:
            group_user_member = GroupUser.objects.filter(user=user).filter(is_owner=False).filter(is_active=True)
            group = CustomGroup.objects.filter(id__in=group_user_member.values_list("group", flat=True))
        serializer = self.serializer_class(group, many=True)
        return Response({"groups": serializer.data}, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        user = request.user
        try:
            group = CustomGroup.objects.get(pk=pk)
        except CustomGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if group.is_active == False:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #check if the user is a member of the group and is active
        try:
            GroupUser.objects.filter(user=user).filter(group=group).filter(is_active=True).get()
        except GroupUser.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN) 
        serializer = self.serializer_class(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if request.data.get("name") is None or request.data.get("description") is None:
            return Response("Invalid request data", status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid()
        instance = CustomGroup.objects.filter(name=request.data.get("name")).all()
        if len(instance) > 0:
            return Response("group name already exits", status=status.HTTP_400_BAD_REQUEST)
        group = CustomGroup.objects.create(name=request.data.get("name"), description=request.data.get("description"))
        GroupUser.objects.create(user=request.user, group=group, is_owner=True, is_active=True)
        serializer = self.serializer_class(group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        user = request.user
        name = request.data.get("name")
        description = request.data.get("description")
        
        if name is None or description is None:
            return Response("Invalid request data", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        try:
            group = CustomGroup.objects.get(pk=pk)
        except CustomGroup.DoesNotExist:
            return Response("Group not found", status=status.HTTP_404_NOT_FOUND)
        if group.is_active == False:
            return Response("Group not found", status=status.HTTP_404_NOT_FOUND)
        group_user = GroupUser.objects.filter(user=user).filter(group=group).filter(is_active=True).filter(is_owner=True)
        if not group_user.exists():
            return Response("User not authorized", status=status.HTTP_403_FORBIDDEN)
        group.name = name
        group.description = description
        group.save()
        serializer = self.serializer_class(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        user = request.user
        try:
            group = CustomGroup.objects.get(pk=pk)
        except CustomGroup.DoesNotExist:
            return Response("Group not found", status=status.HTTP_404_NOT_FOUND)
        if group.is_active == False:
            return Response("Group not found", status=status.HTTP_404_NOT_FOUND)
        group_user = GroupUser.objects.filter(user=user).filter(group=group).filter(is_active=True).filter(is_owner=True)
        if not group_user.exists():
            return Response("User not authorized", status=status.HTTP_403_FORBIDDEN)
        group.is_active = False
        group.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

