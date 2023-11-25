import datetime

import django.conf
from django.urls import reverse
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters import rest_framework as filters

from .models import Order
from .serializers import OrderSerializer
from .filters import OrderFilter
from .logics import make_pay_order, get_payment_status
from car.models import CarRegister


class OrderViewSet(ModelViewSet):
    permission_classes = (AllowAny, )
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter

    def retrieve(self, request, *args, **kwargs):
        car_registers: Queryset = CarRegister.objects.filter(code=kwargs['pk'])
        if len(car_registers) == 0:
            return Response(status=404)
        car_register = car_registers[0]
        car_register.leave_date = datetime.datetime.now()

        notify_url = request.build_absolute_uri(reverse('order-paypal-notify', kwargs=kwargs))
        return_url = request.build_absolute_uri(
            settings.REDIRECT_PAGE.replace("%order%", kwargs['pk'])
        )
        cancel_url = request.build_absolute_uri(reverse('order-paypal-cancel', kwargs=kwargs))
        order, link = make_pay_order(car_register, notify_url, return_url, cancel_url)
        return Response({'link': link}, status=201)

    @action(methods=['get'], detail=True, permission_classes=[AllowAny], url_name='status', url_path='status')
    def order_status(self, request: Request, pk=None):
        car_registers = CarRegister.objects.filter(code=pk)
        if len(car_registers) == 0:
            return Response(status=404)
        car_register = car_registers[0]

        orders = Order.objects.filter(car_register=car_register)
        if len(orders) == 0:
            return Response(status=404)
        order = orders[0]
        order.save()

        status, context = get_payment_status(order)
        if not status:
            Response(data=context, status=401)

        return Response(data=context, status=201)

    @action(methods=['get'], detail=True, permission_classes=[AllowAny], url_name='paypal-cancel')
    def retrieve_cancel(self, request, pk=None):
        return Response(status=201, data=request.data)

    @action(methods=['get'], detail=True, permission_classes=[AllowAny], url_name='paypal-notify')
    def retrieve_notify(self, request, pk=None):
        return Response(status=201, data=request.data)