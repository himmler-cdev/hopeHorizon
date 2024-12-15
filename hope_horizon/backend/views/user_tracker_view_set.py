from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.serializers import UserTrackerSerializer
from backend.models import UserTracker
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers


class UserTrackerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserTrackerSerializer
    queryset = UserTracker.objects.all()

    def list(self, request):
        instance = self.queryset.filter(user_id=request.user).all()
        if len(instance) != 1:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.serializer_class(instance[0])
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid() 
            self._custom_validation(request.data)
        except serializers.ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.queryset.filter(user_id=request.user).all()
        if len(instance) > 0:
            return Response({"detail": "User tracker entry already exits"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        try:
            instance = self.queryset.get(id=pk)
            if instance.user_id != request.user:
                return Response({"detail": "User does not have permission to update this entry"}, status=status.HTTP_403_FORBIDDEN)
        except UserTracker.DoesNotExist:
            return Response({"detail": "User tracker entry does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"detail": "Invalid user tracker entry id"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data)
        try:
            serializer.is_valid() 
            self._custom_validation(request.data)
            serializer.save()
        except serializers.ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def _custom_validation(self, data):
        if "is_enabled" not in data.keys():
            raise serializers.ValidationError("is_enabled field is required")
        if "track_mood" not in data.keys():
            raise serializers.ValidationError("track_mood field is required")
        if "track_energy_level" not in data.keys():
            raise serializers.ValidationError("track_energy_level field is required")
        if "track_sleep_quality" not in data.keys():
            raise serializers.ValidationError("track_sleep_quality field is required")
        if "track_anxiety_level" not in data.keys():
            raise serializers.ValidationError("track_anxiety_level field is required")
        if "track_appetite" not in data.keys():
            raise serializers.ValidationError("track_appetite field is required")
        if "track_content" not in data.keys():
            raise serializers.ValidationError("track_content field is required")