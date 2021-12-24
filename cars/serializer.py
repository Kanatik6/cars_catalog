from rest_framework import serializers

from .models import  Car, CarBrand 


class BrandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CarBrand
        exclude = []
        
# поспрашивать про read_only нужно ли все это в ридонли закидывать
class CarSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    class Meta:
        model = Car
        # exclude = []
        fields = ['id','brand','full_name','price','mileage','year','url','brand']
        
        
class DateSerializer(serializers.Serializer):
    
    