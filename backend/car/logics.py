from .models import Car, CarRegister


def _create_car(patent: str) -> Car:
    """Creates a new car object with the given patent number and adds it to the register"""
    car = Car(patent=patent)
    car.save()
    return car


def get_car(patent: str) -> Car:
    """Returns a car object with the given patent number from the register, or creates and adds it if it does not exist"""
    cars = Car.objects.filter(patent=patent)
    if len(cars) == 0:
        car = _create_car(patent=patent)
    else:
        car = cars[0]
    return car