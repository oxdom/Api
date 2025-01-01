import os
import requests
import hmac
import hashlib
import base64
import json
import time
from dotenv import load_dotenv

load_dotenv()

def place_orders(orders):
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    ts = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    nonce = str(int(time.time() * 1000))
    method = "/v3/orders/place"
    api_url = "api.ox.fun"

    post_data = {
        "recvWindow": 20000,
        "responseType": "FULL",
        "timestamp": int(time.time() * 1000),
        "orders": orders
    }

    body = json.dumps(post_data)
    msg_string = f"{ts}\n{nonce}\nPOST\n{api_url}\n{method}\n{body}"

    sign = base64.b64encode(hmac.new(secret_key, msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'AccessKey': api_key,
        'Timestamp': ts,
        'Signature': sign,
        'Nonce': nonce
    }

    try:
        response = requests.post(f"https://{api_url}{method}", data=body, headers=headers)
        response.raise_for_status()
        print('Response:', response.json())
    except requests.exceptions.RequestException as error:
        print('Error placing orders:', error)

# Example usage
orders = [
    {
        "clientOrderId": 1612249737724,
        "marketCode": "BTC-USD-SWAP-LIN",
        "side": "SELL",
        "quantity": "0.001",
        "timeInForce": "GTC",
        "orderType": "LIMIT",
        "price": "50007"
    },
    {
        "clientOrderId": 1612249737724,
        "marketCode": "BTC-USD-SWAP-LIN",
        "side": "BUY",
        "quantity": "0.002",
        "timeInForce": "GTC",
        "orderType": "LIMIT",
        "price": "54900"
    }
]

place_orders(orders)