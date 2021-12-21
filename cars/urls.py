from django_filters import filters
from rest_framework import routers
from django.urls import path


from .views import CarListView
from .tasks import parse_category

# router = routers.SimpleRouter()
# router.register('model', CarListView)
urlpatterns = [
    path('parse_category/',parse_category),
    path('list_cars/',CarListView.as_view({'get': 'list'}),name='list_cars_url'),
    path('list_cars/filter/', CarListView.as_view({'get': 'filter_price'}))
    ]
# urlpatterns = router.urls

