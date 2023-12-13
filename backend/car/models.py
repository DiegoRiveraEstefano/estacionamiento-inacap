

from django.db import models

# Quota is the amount of money to pay for a minute
quota = 12


class Car(models.Model):
    """
    A car model represents a vehicle with a unique identifier (patent) and a list of registers.
    """

    patent = models.CharField(max_length=8, primary_key=True)
    """
    The patent number is the unique identifier for each car.
    It should be a string of 8 characters.
    """

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def get_registers(self):
        """
        Return all registers associated with this car.
        """
        return self.registers.all()


class CarRegister(models.Model):
    """
    A car register model represents a single entry in the system for a specific car.
    It contains information about the date the car entered and left the parking lot, as well as any associated QR code.
    """

    enter_date = models.DateField(auto_now=True, null=False)
    """
    The date the car entered the parking lot.
    It should be a datetime object.
    """

    leave_date = models.DateField(null=True)
    """
    The date the car left the parking lot.
    It can be null if the car is still in the parking lot.
    """

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="registers")
    """
    The foreign key to the car model.
    """

    code = models.CharField(null=True, max_length=64)
    """
    The QR code associated with this register.
    It can be null if there is no QR code.
    """

    class Meta:
        ordering = ("enter_date", "leave_date")
        get_latest_by = ("enter_date", "leave_date")
        verbose_name = "CarRegister"
        verbose_name_plural = "CarRegisters"

    @property
    def get_qr(self):
        """
        Return the QR code associated with this register, if any.
        Otherwise return an empty string.
        """
        return ""

    def get_price(self):
        """
        Calculate and return the price for this register based on the number of minutwes the car has been in the parking lot.
        The price is calculated as (number of days) * (quota).
        If the leave date is null, then the number of days is (current date - enter date).
        """
        return 100  # (self.enter_date - self.leave_date) * quota