from django_filters import rest_framework as django_filters
from .models import CarBrand, Car

class CarBrandFilter(django_filters.FilterSet):
    brand_name = django_filters.CharFilter(filed_name='brand_name',lookup_expr='')
    
    # class Meta:
    #     model = CarBrand
    #     fields = ['brand_name']
        
class CarFilter(django_filters.FilterSet):
    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_to = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    mileage_from = django_filters.NumberFilter(field_name='mileage', lookup_expr='gte')
    mileage_to = django_filters.NumberFilter(field_name='mileage', lookup_expr='lte')
    
    class Meta:
        model = Car
        fields = ['brand','mileage']
