import base64
import datetime
from django.conf import settings
import requests
from car.models import CarRegister
from .models import Order


def get_paypal_token() -> str:
    client_ID = settings.CLIENT_ID
    client_Secret = settings.CLIENT_SECRET
    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    data = {
        "client_id": client_ID,
        "client_secret": client_Secret,
        "grant_type": "client_credentials"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic {0}".format(base64.b64encode((client_ID + ":" + client_Secret).encode()).decode())
    }

    token = requests.post(url, data, headers=headers)
    return token.json()['access_token']


def make_pay_order(car_register: CarRegister, notify_url, return_url, cancel_url):
    car_register.leave_date = datetime.datetime.now()
    token = get_paypal_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }
    application_context = {
        "notify_url": notify_url,
        "return_url": return_url,
        "cancel_url": cancel_url,
        "brand_name": "Estacionamiento Inacap",
        "landing_page": "BILLING",
        "shipping_preference": "NO_SHIPPING",
        "user_action": "CONTINUE"
    }

    purchase_units = [
        {
            "reference_id": car_register.code,
            "description": "Estacionamiento",

            "custom_id": "CUST-Estacionamiento",
            "soft_descriptor": "Estacionamiento",
            "amount": {
                "currency_code": "USD",
                "value": car_register.get_price(),
            },
        }
    ]

    json_data = {
        "intent": "CAPTURE",
        'application_context': application_context,
        'purchase_units': purchase_units
    }

    response = requests.post(
        'https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, json=json_data)
    payment_id = response.json()['id']
    order = Order(car_register=car_register, payment_id=payment_id)
    order.save()
    linkForPayment = response.json()['links'][1]['href']
    return order, linkForPayment


def get_payment_status(order):
    headers = {'Authorization': f'Bearer {get_paypal_token()}'}
    response = requests.get(
        f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order.payment_id}', headers=headers)

    data = response.json()
    approved = data['status'] == 'APPROVED'
    value = float(data['purchase_units'][0]['amount']['value']) == order.car_register.get_price()

    if not approved:
        return False, {'context': 'No Aprobado'}

    if not value:
        return True, {'context': 'Cantidad Incorrecta'}

    order.paid = True
    order.save()
    return True, {'context': 'Pago Correctamente Realizado'}
