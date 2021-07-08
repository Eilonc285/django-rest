from rest_framework import serializers
from .models import Business


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
            'id', 'title', 'sub_title', 'street', 'number', 'city', 'grade'
        ]
