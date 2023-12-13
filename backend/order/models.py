from django.db import models
from car.models import Car, CarRegister

class Order(models.Model):
    """
    A model to represent orders for cars.
    """

    car_register = models.ForeignKey(CarRegister, on_delete=models.CASCADE)
    """
    The foreign key to the car register model.
    """

    paid = models.BooleanField(default=False)
    """
    A boolean field to indicate if the order is paid or not.
    """

    paid_date = models.DateField(null=True)
    """
    The date when the order was paid. This field is nullable because an order may not be paid yet.
    """

    payment_id = models.CharField(max_length=128, null=False)
    """
    The unique identifier for the payment of this order.
    """

    class Meta:
        ordering = ("paid_date", )
        get_latest_by = ("paid_date", )
        verbose_name = "Order"
        verbose_name_plural = "Orders"
