from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import  Car #carbrand
from .serializer import CarSerializer

class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny,]