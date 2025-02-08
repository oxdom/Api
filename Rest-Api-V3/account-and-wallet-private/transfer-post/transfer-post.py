import os
import requests
import hmac
import hashlib
import base64
import time
import json
from dotenv import load_dotenv

load_dotenv()

def create_transfer(asset, quantity, from_account, to_account):
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    ts = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    nonce = str(int(time.time() * 1000))
    method = "/v3/transfer"
    api_url = "api.ox.fun"

    body = {
        "asset": asset,
        "quantity": quantity,
        "fromAccount": from_account,
        "toAccount": to_account
    }

    # For POST requests, we use the JSON stringified body instead of query params
    body_string = json.dumps(body)
    msg_string = f"{ts}\n{nonce}\nPOST\n{api_url}\n{method}\n{body_string}"

    sign = base64.b64encode(hmac.new(secret_key, msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'AccessKey': api_key,
        'Timestamp': ts,
        'Signature': sign,
        'Nonce': nonce
    }

    try:
        response = requests.post(f"https://{api_url}{method}", json=body, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get('success'):
            return data['data']
        else:
            print('Failed to create transfer')
    except requests.exceptions.RequestException as error:
        print('Error creating transfer:', error)

# Example usage
asset = 'USDT'
quantity = '1000'
from_account = '14320'
to_account = '15343'

response = create_transfer(asset, quantity, from_account, to_account)
print(response)
