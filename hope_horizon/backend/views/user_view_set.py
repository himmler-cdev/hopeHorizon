from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.serializers import (
    UserCreateUpdateSerializer,
    UserListSerializer,
    UserDetailsSerializer,
)
from backend.models import User, UserRole
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import date


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializers = {
        "create": UserCreateUpdateSerializer,
        "update": UserCreateUpdateSerializer,
        "list": UserListSerializer,
        "details": UserDetailsSerializer,
    }

    def list(self, request):
        pass

    def create(self, request):
        serializer = self.serializers["create"](data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = serializer.save()
            user.set_password(serializer.data["password"])
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializers["details"](user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response("User not authenticated", status=status.HTTP_401_UNAUTHORIZED)
        try:
            instance = self.queryset.get(id=pk)
            if instance.user_id != request.user:
                return Response("User does not have permission to update this entry", status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializers["update"](instance, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        serializer = self.serializers["details"](user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        pass
