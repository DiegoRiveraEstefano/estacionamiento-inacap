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
    permission_classes = (AllowAny, )
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CarFilter

    def create(self, request: Request, *args, **kwargs):
        serialized_car = self.serializer_class(data=request.data)
        if not serialized_car.is_valid():
            return Response(status=401)

        car = serialized_car.save()
        if not car:
            return Response(status=401)

        return Response(status=201, data=serialized_car.data)


class CarRegisterViewSet(ModelViewSet):
    permission_classes = (AllowAny, )
    serializer_class = CarRegisterSerializer
    queryset = CarRegister.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CarRegisterFilter

    def create(self, request, *args, **kwargs):
        car = get_car(request.data['patent'])
        serialized_register_car = self.serializer_class(
            data={'car': car.patent})

        serialized_register_car.is_valid(raise_exception=True)
        car_register: CarRegister = serialized_register_car.save()

        serialized_register_car = self.serializer_class(
            car_register, data={'code': hash(f"{car.patent}-{car_register.enter_date}")}, partial=True)

        serialized_register_car.is_valid(raise_exception=True)
        serialized_register_car.save()

        return Response(data=serialized_register_car.data, status=201)