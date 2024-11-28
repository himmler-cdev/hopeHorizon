from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.serializers import UserStatusSerializer
from backend.models import UserStatus
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import date


class UserStatusViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = UserStatusSerializer
    queryset = UserStatus.objects.all()

    def list(self, request):
        from_date = request.query_params.get('from', None)
        to_date = request.query_params.get('to', None)
        if from_date is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        instance = self.queryset.filter(user=request.user)
        instance = instance.filter(Q(date__gte=from_date))
        if to_date is not None:
            instance = instance.filter(Q(date__lte=to_date))
        serializer = self.serializer_class(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        instance = self.queryset.filter(Q(user=request.user) & Q(date=date.today())).all()
        if len(instance) > 0:
            return Response("User status entry already exits", status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        