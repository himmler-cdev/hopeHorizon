from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend.models import Notification
from backend.serializers import NotificationSerializer
from django.db.models import Q


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()

    def list(self, request):
        is_read = request.query_params.get('is_read', None)
        instance = self.queryset.filter(user=request.user)

        if is_read is not None:
            instance = instance.filter(is_read=is_read)

        serializer = NotificationSerializer(instance, many=True)
        return Response({"notifications": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request):
        #Create a new notification for the authenticated user.

        serializer = NotificationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)  # Automatically set the user
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        try:
            # Retrieve the notification for the logged-in user
            instance = self.queryset.get(pk=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response(
                {"detail": "Notification not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Use NotificationDetailSerializer to update
        serializer = NotificationSerializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save the updated notification
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        #Delete a notification for the authenticated user.
    
        try:
            instance = self.queryset.get(pk=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response(
                {"detail": "Notification not found."}, status=status.HTTP_404_NOT_FOUND
            )

        instance.delete()
        return Response({"detail": "Notification deleted."}, status=status.HTTP_204_NO_CONTENT)
