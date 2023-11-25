from .models import Car, CarRegister


def _create_car(patent: str) -> Car:
    car = Car(patent=patent)
    car.save()
    return car


def get_car(patent: str) -> Car:
    cars = Car.objects.filter(patent=patent)
    if len(cars) == 0:
        car = _create_car(patent=patent)
    else:
        car = cars[0]
    return car
