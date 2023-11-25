from django.db import models
from car.models import Car, CarRegister


class Order(models.Model):
    car_register = models.ForeignKey(CarRegister, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True)
    payment_id = models.CharField(max_length=128, null=False)

    class Meta:
        ordering = ("paid_date", )
        get_latest_by = ("paid_date", )
        verbose_name = "Order"
        verbose_name_plural = "Orders"
