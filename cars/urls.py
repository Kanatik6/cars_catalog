from django.urls import path

from .models import CarBrand
from .views import CarListView, CarDetailView,BrandListView,BrandDetailView, min_max

urlpatterns = [
    path('list_cars/',CarListView.as_view({'get': 'list'}),name='list_cars_url'),
    path('list_cars/filter/', CarListView.as_view({'get': 'filter_price'}),name='list_cars_filter_url'),
    path('list_cars/<int:pk>/',CarDetailView.as_view({'get':'list'}),name='cars_detail_url'),
    path('list_brands/',BrandListView.as_view({'get':'list'}),name='list_brand_url'),
    path('list_brands/<int:pk>/',BrandDetailView.as_view({'get':'list'}),name='detail_brand_url'),
    path('min_max/',min_max,name='min_max_url')
    ]
