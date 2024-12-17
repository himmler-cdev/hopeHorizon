from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.models import Notification
from backend.serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def list(self, request):
        notifications = Notification.objects.filter(user_id=request.user, is_read=False).order_by('-date')
        serializer = NotificationSerializer(notifications, many=True)

        return Response({"notifications": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            notification = Notification.objects.get(id=pk)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"detail": "Invalid ID"}, status=status.HTTP_400_BAD_REQUEST)

        if notification.user_id != request.user:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
