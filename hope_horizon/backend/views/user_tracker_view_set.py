from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.serializers import UserTrackerSerializer
from backend.models import UserTracker
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import date


class UserTrackerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserTrackerSerializer
    queryset = UserTracker.objects.all()

    def list(self, request):
        instance = self.queryset.filter(user_id=request.user).all()
        if len(instance) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.serializer_class(instance[0])
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not self._custom_validation(request):
            return Response("Invalid request data", status=status.HTTP_400_BAD_REQUEST)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        instance = self.queryset.filter(user=request.user).all()
        if len(instance) > 0:
            return Response("User tracker entry already exits", status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        try:
            instance = self.queryset.get(id=pk)
        except UserTracker.DoesNotExist:
            return Response("User tracker entry does not exist", status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data)
        if not self._custom_validation(request):
            return Response("Invalid request data", status=status.HTTP_400_BAD_REQUEST)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def _custom_validation(self, request):
        if request.data.get("is_enabled") is None:
            return False
        if request.data.get("track_mood") is None:
            return False
        if request.data.get("track_energy_level") is None:
            return False
        if request.data.get("track_sleep_quality") is None:
            return False
        if request.data.get("track_anxiety_level") is None:
            return False
        if request.data.get("track_appetite") is None:
            return False
        if request.data.get("track_content") is None:
            return False
        return True
        