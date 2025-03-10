# users/serializers.py
from rest_framework import serializers
from .models import SampleModel

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleModel
        fields = ['id', 'name', 'age']
