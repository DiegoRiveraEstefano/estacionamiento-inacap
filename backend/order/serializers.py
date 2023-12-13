from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    This class is responsible for serializing and deserializing order data.

    Attributes:
        model (Order): The model that this serializer is associated with.
        fields (list): A list of fields to include in the serialization.
        paid_date (DateField): A field for storing the date when the order was paid.
        paid (BooleanField): A field for storing whether the order has been paid or not.
        payment_url (URLField): A field for storing the URL of the payment page.
    """

    paid_date = serializers.DateField(required=False)
    paid = serializers.BooleanField(required=False, default=False)
    payment_url = serializers.URLField(required=False, default="")


    class Meta:
        model = Order
        fields = ["car_register", "paid", "paid_date", 'payment_url']
