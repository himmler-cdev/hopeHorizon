from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.serializers import UserStatusSerializer
from backend.models import UserStatus
from rest_framework.permissions import IsAuthenticated


class UserStatusViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = UserStatusSerializer
    queryset = UserStatus.objects.all()

    def list(self, request):
        # retrive all user statuses for the logged in/current user
        instance = self.get_queryset().filter(user=request.user)

        # serialize the data
        serializer = self.serializer_class(instance, many=True)

        # return the data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        # create a new user status instance of the request data
        instance = self.get_serializer(data=request.data)

        # check if the data is valid
        if instance.is_valid():

            # save the data into the database
            instance.save()

            # return the data
            return Response(instance.data, status=status.HTTP_201_CREATED)

        # return an error if the data is not valid
        return Response(instance.errors, status=status.HTTP_400_BAD_REQUEST)
