from django_filters import filters
from rest_framework import routers
from django.urls import path

from cars.models import CarBrand


from .views import CarListView, CarDetailView,BrandListView,BrandDetailView
from .tasks import parse_category

# router = routers.SimpleRouter()
# router.register('model', CarListView)
urlpatterns = [
    path('parse_category/',parse_category),
    path('list_cars/',CarListView.as_view({'get': 'list'}),name='list_cars_url'),
    path('list_cars/filter/', CarListView.as_view({'get': 'filter_price'}),name='list_cars_filter_url'),
    path('list_cars/<int:pk>/',CarDetailView.as_view({'get':'list'}),name='cars_detail_url'),
    path('list_brands/',BrandListView.as_view({'get':'list'}),name='list_brand_url'),
    path('list_brands/<int:pk>',BrandDetailView.as_view({'get':'list'}),name='detail_brand_url'),
    ]
# urlpatterns = router.urls

