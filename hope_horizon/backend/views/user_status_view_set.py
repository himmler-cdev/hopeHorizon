from django.forms import ValidationError
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
        try:
            if from_date is None:
                return Response({"detail": "From data must be set"}, status=status.HTTP_400_BAD_REQUEST)
            instance = self.queryset.filter(user_id=request.user).all()
            instance = instance.filter(Q(date__gte=from_date))
            if to_date is not None:
                instance = instance.filter(Q(date__lte=to_date))
            serializer = self.serializer_class(instance, many=True)
            return Response({"user_statuses": serializer.data}, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({"detail": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        instance = self.queryset.filter(Q(user_id=request.user) & Q(date=date.today())).all()
        if len(instance) > 0:
            return Response({"detail": "User status entry already exits"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
