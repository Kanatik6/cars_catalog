from rest_framework import routers

from .views import CarViewSet

router = routers.SimpleRouter()
router.register(r'model', CarViewSet)
urlpatterns = []
urlpatterns = router.urls
