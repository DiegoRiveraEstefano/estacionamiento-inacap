from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    paid_date = serializers.DateField(required=False)
    paid = serializers.BooleanField(required=False, default=False)
    payment_url = serializers.URLField(required=False, default="")

    class Meta:
        model = Order
        fields = ["car_register", "paid", "paid_date", 'payment_url']
