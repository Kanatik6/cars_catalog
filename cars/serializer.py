from rest_framework import serializers

from .models import  Car # CarBrand,

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        exclude = []

