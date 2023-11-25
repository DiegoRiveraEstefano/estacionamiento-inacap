from django.urls import path
from rest_framework import routers
from .views import OrderViewSet


urlpatterns = [
    #path('pay/return/', (), name="paypal-return-url"),
    #path('pay/return/', (), name="pdt_return_url"),
    #path('pay/return/', (), name="pdt_return_url"),
]

routers = routers.SimpleRouter()
routers.register('order', OrderViewSet)


urlpatterns += routers.urls


