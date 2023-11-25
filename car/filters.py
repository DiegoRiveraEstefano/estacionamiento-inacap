from .models import Car, CarRegister
from django_filters import rest_framework as filters


class CarFilter(filters.FilterSet):

    class Meta:
        model = Car
        fields = {
            "patent": ["iexact"]
        }


class CarRegisterFilter(filters.FilterSet):
    class Meta:
        model = CarRegister
        fields = {
            "car__patent": ["iexact"],
            "enter_date": ["iexact", "gte", "lte"],
            "leave_date": ["iexact", "gte", "lte"],
            "code": ["iexact"],
        }