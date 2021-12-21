from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from rest_framework import generics, serializers, status
from django.db.models import Max
from decimal import Decimal as D
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins

from .models import  Car 
from .serializer import CarSerializer

class CarListView(mixins.ListModelMixin, GenericViewSet):
    
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny,]
    
    @action(methods=['get'], detail=False)
    def filter_price(self, request, *args, **kwargs):
        min_price = self.request.GET.get('min_price',0)
        max_price = self.request.GET.get('max_price',self.queryset.aggregate(Max('price'))['price__max'])
        print(min_price,max_price)
        if [min_price,max_price] == [None,None]:
            serializer = self.serializer_class(self.queryset,many=True)
            return Response(serializer.data)
        
        result_queryset = self.queryset.filter(price__gte=min_price,price__lte=max_price)
        serializer = self.serializer_class(result_queryset,many=True)
        return Response(serializer.data)

