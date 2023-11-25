from rest_framework import routers
from .views import CarRegisterViewSet

router = routers.SimpleRouter()
router.register(r'car_register', CarRegisterViewSet)

urlpatterns = router.urls