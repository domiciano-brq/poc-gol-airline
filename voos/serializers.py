from rest_framework import serializers
from .models import Voo


class VooSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voo
        fields = '__all__'


class VooDetalheSerializer(VooSerializer):
    pass
