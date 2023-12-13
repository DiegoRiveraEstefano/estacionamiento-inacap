from .models import Order
from django_filters import rest_framework as filters


class OrderFilter(filters.FilterSet):
    """
    This class represents a filter for the Order model. It allows filtering by car_register__car__patent, paid, and paid_date.
    """

    class Meta:
        """
        This class contains metadata about the filter.
        """
        model = Order
        fields = {
            "car_register__car__patent": ["iexact"],
            'paid': ["exact"],
            "paid_date": ["iexact", "gte", "lte"],
        }
