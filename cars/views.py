from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from rest_framework import generics, status

from .models import  Car 
from .serializer import CarSerializer
from .filters CarFilterByPriceRange

class CarListView(generics.ListAPIView):
    
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny,]
    filter_backends = [django_filters.DjangoFilterBackend,]
    filterset_class = CarFilterByPriceRange
    
    # ? как тут реализовать фильтр по цене
    def get_queryset(self):
        if [self.request.GET.get('min_price'),self.request.GET.get('max_price')] == [None,None]:    
            return super().get_queryset(self)            
        self.filter = self.filterset_class(self.request.GET, queryset=Car.objects.all())
        return self.filter.qs

        
