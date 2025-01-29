from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.serializers import QuoteSerializer
from rest_framework.permissions import IsAuthenticated
from backend.models import Quote
import random


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = QuoteSerializer

    def list(self, request):
        quotes = self.queryset
        random_quote = random.choice(quotes)
        serializer = QuoteSerializer(random_quote)
        return Response(serializer.data, status=status.HTTP_200_OK)