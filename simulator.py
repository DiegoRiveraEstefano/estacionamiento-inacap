import requests
import json


def main():
    url = "http://127.0.0.1:8000/car/"

    payload = json.dumps({
        "patent": input('ingrese la patente\n')
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("Ingrese a la siguiente url para pagar http://localhost:4321/")
    print("E Ingrese su codigo de entrada")
    print(response.json()['code'])

if __name__ == '__main__':
    main()
