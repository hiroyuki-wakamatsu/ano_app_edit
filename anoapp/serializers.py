from rest_framework import serializers
from .models import AnotherQuotationHeader


class AnotherQuotationHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnotherQuotationHeader
        fields = "__all__"
