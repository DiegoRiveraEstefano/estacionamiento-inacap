from rest_framework import routers
from .views import CarRegisterViewSet

# Register a viewset with the router for the 'car' URL pattern.
router = routers.SimpleRouter()
router.register(r'car', CarRegisterViewSet)

urlpatterns = router.urls