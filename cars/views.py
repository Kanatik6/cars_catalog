from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import  Car, CarBrand 
from .serializer import BrandSerializer, CarSerializer
from .filters import CarFilter, PageNumberPagination


    

class CarListView(mixins.ListModelMixin, GenericViewSet):
    
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny,]
    filter_backends = [django_filters.DjangoFilterBackend, SearchFilter]
    # filter_fields = ['price', 'mileage']
    filterset_class = CarFilter
    filter_fields = ['full_name', ]
    search_fields = ['full_name', ]
    pagination_class = PageNumberPagination
    def get_queryset(self):
        return_qs = self.queryset.order_by('id')
        return super().get_queryset()
    
class CarDetailView(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny,]

class BrandListView(mixins.ListModelMixin,GenericViewSet):
    queryset = CarBrand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny,]
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        return_qs = self.queryset.order_by('brand_name')
        return super().get_queryset()
    
class BrandDetailView(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = CarBrand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny,]
    
# для выпадающего списка
@api_view(['GET'])
def min_max(request):
    cars_year = Car.objects.order_by('year')
    min_year = cars_year.first().year
    max_year = cars_year.last().year
    cars_mileage = Car.objects.order_by('mileage')
    min_mileage = cars_mileage.first().mileage
    max_mileage = cars_mileage.last().mileage
    return Response({'min_year':min_year,
                     'max_year':max_year,
                     'min_mileage':min_mileage,
                     'max_mileage':max_mileage})

