from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters import rest_framework as filters

from .models import Car, CarRegister
from .serializers import CarSerializer, CarRegisterSerializer
from .filters import CarFilter, CarRegisterFilter
from .logics import get_car


class CarViewSet(ModelViewSet):
    """This class is responsible for handling HTTP requests related to cars.

    The following methods are available:

    * GET: Retrieve all cars in the database
    * POST: Create a new car in the database
    * DELETE: Delete a car from the database
    """
    permission_classes = (AllowAny, )
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CarFilter

    def create(self, request: Request, *args, **kwargs):
        """This method is responsible for creating a new car in the database.

        The following steps are performed:

        * Validate the incoming data against the CarSerializer
        * Create a new instance of the Car model with the validated data
        * Save the instance to the database
        * Return the newly created car in JSON format
        """
        serialized_car = self.serializer_class(data=request.data)

        # Check if the incoming data is valid
        if not serialized_car.is_valid():
            return Response(status=401)

        car = serialized_car.save()

        # Check if the car was successfully created
        if not car:
            return Response(status=401)

        return Response(status=201, data=serialized_car.data)


class CarRegisterViewSet(ModelViewSet):
    """
    Provides an API endpoint to view and manipulate car register records.
    """

    permission_classes = (AllowAny,)
    serializer_class = CarRegisterSerializer
    queryset = CarRegister.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CarRegisterFilter

    def create(self, request, *args, **kwargs):
        """
        Creates a new car register record.

        :param request: The HTTP request object.
        :type request: django.http.request
        :param args: The positional arguments for the method.
        :type args: list
        :param kwargs: The keyword arguments for the method.
        :type kwargs: dict
        """

        # Get the car object from the request data
        car = get_car(request.data['patent'])

        # Create a new serializer instance with the car object and validate it
        serialized_register_car = self.serializer_class(data={'car': car.patent})
        serialized_register_car.is_valid(raise_exception=True)

        # Save the serializer to the database and get the new car register object
        car_register = serialized_register_car.save()

        # Create a new serializer instance with the code field and set it as partial
        serialized_register_car = self.serializer_class(car_register, data={'code': hash(f"{car.patent}-{car_register.enter_date}")}, partial=True)

        # Validate the new serializer instance and save it to the database
        serialized_register_car.is_valid(raise_exception=True)
        serialized_register_car.save()

        return Response(data=serialized_register_car.data, status=201)