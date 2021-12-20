from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from rest_framework import generics, status

from .models import  Car 
from .serializer import CarSerializer

class CarListView(generics.ListAPIView):
    
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        
        if [min_price,max_price] == [None,None]:    
            return super().get_queryset()
        
        result_queryset = self.queryset.filter(price__gte=min_price,price__lte=max_price)
        return result_queryset
