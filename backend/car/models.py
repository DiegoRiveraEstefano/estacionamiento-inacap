from django.db import models

quota = 12


class Car(models.Model):
    patent = models.CharField(max_length=8, primary_key=True)

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def get_registers(self):
        return self.registers.all()


class CarRegister(models.Model):
    enter_date = models.DateField(auto_now=True, null=False)
    leave_date = models.DateField(null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="registers")
    code = models.CharField(null=True, max_length=64)

    class Meta:
        ordering = ("enter_date", "leave_date")
        get_latest_by = ("enter_date", "leave_date")
        verbose_name = "CarRegister"
        verbose_name_plural = "CarRegisters"

    @property
    def get_qr(self):
        return ""

    def get_price(self):
        return 100  # (self.enter_date - self.leave_date) * quota
