import os
import requests
import hmac
import hashlib
import base64
import json
import time
from dotenv import load_dotenv

load_dotenv()

def cancel_all_orders(market_code):
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    ts = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    nonce = str(int(time.time() * 1000))
    method = "/v3/orders/cancel-all"
    api_url = "api.ox.fun"

    post_data = {
        "marketCode": market_code
    }

    body = json.dumps(post_data)
    msg_string = f"{ts}\n{nonce}\nDELETE\n{api_url}\n{method}\n{body}"

    sign = base64.b64encode(hmac.new(secret_key, msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'AccessKey': api_key,
        'Timestamp': ts,
        'Signature': sign,
        'Nonce': nonce
    }

    try:
        response = requests.delete(f"https://{api_url}{method}", data=body, headers=headers)
        response.raise_for_status()
        print('Response:', response.json())
    except requests.exceptions.RequestException as error:
        print('Error canceling all orders:', error)

# Example usage
cancel_all_orders("BTC-USD-SWAP-LIN")