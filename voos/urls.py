from rest_framework.routers import DefaultRouter
from .views import VooViewSet

router = DefaultRouter()
router.register(r'voos', VooViewSet, basename='voo')

urlpatterns = router.urls
