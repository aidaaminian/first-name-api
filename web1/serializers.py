from rest_framework import serializers
from .models import FirstName

class FirstNameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return FirstName.objects.create(**validated_data)