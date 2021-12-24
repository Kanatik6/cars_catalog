from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from rest_framework import generics, serializers, status
from django.db.models import Max
from decimal import Decimal as D
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.filters import SearchFilter

from .models import  Car, CarBrand 
from .serializer import BrandSerializer, CarSerializer
from .filters import CarFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response


    

class CarListView(mixins.ListModelMixin, GenericViewSet):
    
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny,]
    filter_backends = [django_filters.DjangoFilterBackend, SearchFilter]
    # filter_fields = ['price', 'mileage']
    filterset_class = CarFilter
    filter_fields = ['full_name', ]
    search_fields = ['full_name', ]
    
    
    
    # @action(methods=['get'], detail=False)
    # def filter_price(self, request, *args, **kwargs):
    #     min_price = self.request.GET.get('min_price',0)
    #     max_price = self.request.GET.get('max_price',self.queryset.aggregate(Max('price'))['price__max'])
    #     print(min_price,max_price)
    #     if [min_price,max_price] == [None,None]:
    #         serializer = self.serializer_class(self.queryset,many=True)
    #         return Response(serializer.data)
        
    #     result_queryset = self.queryset.filter(price__gte=min_price,price__lte=max_price)
    #     serializer = self.serializer_class(result_queryset,many=True)
    #     return Response(serializer.data)
    
class CarDetailView(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny,]

class BrandListView(mixins.ListModelMixin,GenericViewSet):
    queryset = CarBrand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny,]
    
    def get_queryset(self):
        return super().get_queryset()
    
class BrandDetailView(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = CarBrand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny,]
    
    def get_queryset(self):
        return super().get_queryset()
    
# class 

@api_view(['GET'])
def min_max(request):
    cars = Car.objects.order_by('year')
    min_year = cars.first().year
    max_year = cars.last().year
    return Response({'min_year':min_year,'max_year':max_year})

