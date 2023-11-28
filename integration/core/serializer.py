from rest_framework import serializers
from integration.core.models import *


class FuzzySerializer(serializers.Serializer):
    field1 = serializers.CharField()
    field2 = serializers.IntegerField()
    # Adicione mais campos conforme necessário


