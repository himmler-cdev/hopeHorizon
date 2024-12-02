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
        search = request.query_params.get("search", None)
        if not request.user.is_authenticated:
            return Response("User not authenticated", status=status.HTTP_401_UNAUTHORIZED)
        instance = self.queryset.filter(is_active=True)
        if search:
            instance = instance.filter(Q(username__icontains=search))
        serializer = self.serializers["list"](instance, many=True)
        return Response({"users": serializer.data}, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.serializers["create"](data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        user.set_password(serializer.data["password"])
        user.save()
        serializer = self.serializers["details"](user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        if not request.user.is_authenticated:
            return Response("User not authenticated", status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = User.objects.get(username=pk)
            serializer = self.serializers['details'](user)
            if user != request.user:
                return Response("User does not have permission to view this entry", status=status.HTTP_403_FORBIDDEN)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        if not request.user.is_authenticated:
            return Response("User not authenticated", status=status.HTTP_401_UNAUTHORIZED)
        try:
            instance = self.queryset.get(id=pk)
            if instance != request.user:
                return Response("User does not have permission to update this entry", status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializers["update"](instance, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        user.set_password(serializer.data["password"])
        user.save()
        serializer = self.serializers["details"](user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response("User not authenticated", status=status.HTTP_401_UNAUTHORIZED)
        try:
            instance = self.queryset.get(id=pk)
            if instance != request.user:
                return Response("User does not have permission to delete this entry", status=status.HTTP_403_FORBIDDEN)
            instance.is_active = False
            instance.save()
            return Response("User deleted", status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
