from rest_framework import serializers
from backend.models import Quote


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ["id", "quote", "author"]
        read_only_fields = ["id", "quote", "author"]