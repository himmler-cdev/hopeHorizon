from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.serializers import GroupSerializer, GroupUserSerializer
from backend.models import CustomGroup, GroupUser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class_group = GroupSerializer
    serializer_class_group_user = GroupUserSerializer

    def list(self, request):
        user = request.user
        owned = request.query_params.get('owned', None)
        
        if owned is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if owned.lower() == 'true':
            group_user_owned = GroupUser.objects.filter(user=user).filter(owner=True).filter(is_active=True)
            group = CustomGroup.objects.filter(id__in=group_user_owned.values_list('group', flat=True))
        else:
            group_user_member = GroupUser.objects.filter(user=user).filter(owner=False).filter(is_active=True)
            group = CustomGroup.objects.filter(id__in=group_user_member.values_list('group', flat=True))

        serializer = self.serializer_class_group(group, many=True)
        return Response({"groups": serializer.data}, status=status.HTTP_200_OK)
    
    def list(self, request, pk=None):
        user = request.user

        try:
            group = CustomGroup.objects.get(pk=pk)
        except CustomGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if CustomGroup.objects.filter(pk=pk).filter(is_active=False):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if user != GroupUser.objects.filter(user=user).filter(group=group).filter(is_active=True).user:
            return Response(status=status.HTTP_403_FORBIDDEN) 
        
        serializer = self.serializer_class_group(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def create(self, request):
        #TODO: Add group creation logic


