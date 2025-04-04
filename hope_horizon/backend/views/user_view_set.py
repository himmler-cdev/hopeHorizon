from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.serializers import (
    UserCreateSerializer,
    UserUpdateSerializer,
    UserListSerializer,
    UserDetailsSerializer,
)
from backend.models import User, UserRole, UserTracker
from django.db.models import Q


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializers = {
        "create": UserCreateSerializer,
        "update": UserUpdateSerializer,
        "list": UserListSerializer,
        "details": UserDetailsSerializer,
    }

    def list(self, request):
        search = request.query_params.get("search", None)
        if not request.user.is_authenticated:
            return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        instance = self.queryset.filter(is_active=True)
        if search:
            instance = instance.filter(Q(username__icontains=search))
        serializer = self.serializers["list"](instance, many=True)
        return Response({"users": serializer.data}, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.serializers["create"](data=request.data)
        if not serializer.is_valid():
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save(user_role_id=UserRole.objects.get(role="User"))
        user.set_password(serializer.data["password"])
        user.save()
        serializer = self.serializers["details"](user)
        UserTracker.objects.create(
            user_id=user,
            is_enabled=True,
            track_mood=True,
            track_energy_level=True,
            track_sleep_quality=True,
            track_anxiety_level=True,
            track_appetite=True,
            track_content=True,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = User.objects.get(username=pk)
            serializer = self.serializers['details'](user)
            if user != request.user:
                return Response({"detail": "User does not have permission to view this entry"}, status=status.HTTP_403_FORBIDDEN)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            instance = self.queryset.get(id=pk)
            if instance != request.user:
                return Response({"detail": "User does not have permission to update this entry"}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"detail": "Invalid user id"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializers["update"](instance, data=request.data)
        if not serializer.is_valid():
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        user.save()
        serializer = self.serializers["details"](user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response("User not authenticated", status=status.HTTP_401_UNAUTHORIZED)
        try:
            instance = self.queryset.get(id=pk)
            if instance != request.user:
                return Response({"detail": "User does not have permission to update this entry"}, status=status.HTTP_403_FORBIDDEN)
            instance.is_active = False
            instance.save()
            return Response("User deleted", status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"detail": "Invalid user id"}, status=status.HTTP_400_BAD_REQUEST)
