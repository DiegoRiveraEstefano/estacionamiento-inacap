from .models import Order
from django_filters import rest_framework as filters


class OrderFilter(filters.FilterSet):

    class Meta:
        model = Order
        fields = {
            "car_register__car__patent": ["iexact"],
            'paid': ["exact"],
            "paid_date": ["iexact", "gte", "lte"],
        }
