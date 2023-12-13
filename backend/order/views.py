import datetime  # Importing the datetime module for date and time related operations.
from django.conf import settings  # Importing settings from Django configuration.
from django.urls import reverse  # Importing reverse function to generate URLs.
from django.conf import settings  # Importing settings from Django configuration.
from rest_framework.decorators import action  # Importing decorator for defining custom actions in viewsets.
from rest_framework.generics import get_object_or_404  # Importing function to get an object or return a 404 error if it doesn't exist.
from rest_framework.request import Request  # Importing Request class from Django Rest Framework.
from rest_framework.response import Response  # Importing Response class from Django Rest Framework.
from rest_framework.viewsets import ModelViewSet  # Importing ModelViewSet class for managing views in Django Rest Framework.
from rest_framework.permissions import AllowAny, IsAuthenticated  # Importing permission classes for controlling access to views.
from django_filters import rest_framework as filters  # Importing filters module from Django Filters library.

from .models import Order  # Importing Order model from the current app.
from .serializers import OrderSerializer  # Importing serializer class for converting data between Python and JSON formats.
from .filters import OrderFilter  # Importing filter class for filtering queryset based on specific criteria.
from .logics import make_pay_order, get_payment_status  # Importing utility functions for payment processing.
from car.models import Car, CarRegister  # Importing Car and CarRegister models from the "backend.car" app.


# Creating a viewset class that inherits from ModelViewSet to manage views related to Order model.
class OrderViewSet(ModelViewSet):
    permission_classes = (AllowAny,)  # Setting permission classes to allow unauthenticated access to this viewset.
    serializer_class = OrderSerializer  # Setting the default serializer class for this viewset.
    queryset = Order.objects.all()  # Setting the queryset to retrieve all Order objects.
    filter_backends = (filters.DjangoFilterBackend,)  # Setting filter backend to apply filters on queryset.
    filterset_class = OrderFilter  # Setting the default filter class for this viewset.

    # Overriding the `retrieve` method to handle specific logic when retrieving an order.
    def retrieve(self, request, *args, **kwargs):
        car_registers = CarRegister.objects.filter(code=kwargs['pk'])  # Finding car register with the provided code.
        if len(car_registers) == 0:  # If no car register is found, return a 404 error.
            return Response(status=404)
        car_register = car_registers[0]  # Selecting the first car register found.
        car_register.leave_date = datetime.datetime.now()  # Setting the leave date of the car register to current date and time.

        notify_url = request.build_absolute_uri(reverse('order-paypal-notify', kwargs=kwargs))  # Building absolute URL for PayPal notification.
        return_url = request.build_absolute_uri(settings.REDIRECT_PAGE.replace("%order%", kwargs['pk']))  # Building absolute URL for redirect after successful payment.
        cancel_url = request.build_absolute_uri(reverse('order-paypal-cancel', kwargs=kwargs))  # Building absolute URL for PayPal cancellation.
        order, link = make_pay_order(car_register, notify_url, return_url, cancel_url)  # Creating and returning the payment details.
        return Response({'link': link}, status=201)  # Returning a response with the payment link.

    # Overriding the `order_status` action to handle specific logic for retrieving order status.
    @action(methods=['get'], detail=True, permission_classes=[AllowAny], url_name='status', url_path='status')
    def order_status(self, request: Request, pk=None):
        car_registers = CarRegister.objects.filter(code=pk)  # Finding car register with the provided code.
        if len(car_registers) == 0:  # If no car register is found, return a 404 error.
            return Response(status=404)
        car_register = car_registers[0]  # Selecting the first car register found.

        orders = Order.objects.filter(car_register=car_register)  # Finding orders related to the car register.
        if len(orders) == 0:  # If no order is found, return a 404 error.
            return Response(status=404)
        order = orders[0]  # Selecting the first order found.
        order.save()  # Saving the order to update any related fields.

        status, context = get_payment_status(order)  # Getting payment status and associated context.
        if not status:  # If payment status is not successful, return a response with error details.
            return Response(data=context, status=401)

        return Response(data=context, status=201)  # Returning a response with the payment status and context.

    # Overriding the `retrieve_cancel` action to handle specific logic for PayPal cancellation.
    @action(methods=['get'], detail=True, permission_classes=[AllowAny], url_name='paypal-cancel', url_path='cancel')
    def retrieve_cancel(self, request):
        return Response(status=201)  # Returning a response with a status code indicating cancellation.

    # Overriding the `retrieve_notify` action to handle specific logic for PayPal notification.
    @action(methods=['get'], detail=True, permission_classes=[AllowAny], url_name='paypal-notify', url_path='notify')
    def retrieve_notify(self, request):
        return Response(status=201)  # Returning a response with a status code indicating notification.