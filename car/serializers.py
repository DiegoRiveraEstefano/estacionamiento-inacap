from rest_framework import serializers
from .models import Car, CarRegister


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ["patent"]


class CarRegisterSerializer(serializers.ModelSerializer):
    leave_date = serializers.DateField(required=False)
    code = serializers.CharField(required=False, max_length=64)
    enter_date = serializers.DateField(required=False)

    class Meta:
        model = CarRegister
        fields = ["enter_date", "leave_date", "car", 'code']
