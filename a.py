import requests

CLIENT_ID = b"AU6d_PFt53dWpdB5rc_Y2tt2taeJZLcoy9pj8UTNFVoL3bQZEQRnVo5JgzxWDUt5LNjaFO5MnFqzq-Un"  # os.getenv("PAYPAL_CLIENT_ID")
CLIENT_SECRET = b"EPRoktuNQ4EIPe4vwX5391RU9dlTi-2UvgPfLHsKcUmFpScO3AfyVFnsYHXX08psIElMqnc6k-bM8R9q"  # os.getenv("PAYPAL_CLIENT_SECRET")

PAYPAL_IDENTITY_TOKEN = requests.request(
    url="https://api-m.sandbox.paypal.com/v1/oauth2/token",
    method="POST",
    auth=(CLIENT_ID, CLIENT_SECRET),
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data="grant_type=client_credentials",
)

print(PAYPAL_IDENTITY_TOKEN.json())