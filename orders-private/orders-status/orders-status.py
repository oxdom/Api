import os
import requests
import hmac
import hashlib
import base64
import time
from dotenv import load_dotenv

load_dotenv()

def fetch_order_status(order_id=None, client_order_id=None):
    if not order_id and not client_order_id:
        raise ValueError("Either orderId or clientOrderId must be provided.")

    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    ts = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    nonce = str(int(time.time() * 1000))
    method = "/v3/orders/status"
    api_url = "api.ox.fun"

    query_string = f"orderId={order_id}" if order_id else f"clientOrderId={client_order_id}"
    msg_string = f"{ts}\n{nonce}\nGET\n{api_url}\n{method}\n{query_string}"

    sign = base64.b64encode(hmac.new(secret_key, msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'AccessKey': api_key,
        'Timestamp': ts,
        'Signature': sign,
        'Nonce': nonce
    }

    try:
        response = requests.get(f"https://{api_url}{method}?{query_string}", headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get('success'):
            return data
        else:
            print('Failed to fetch order status')
    except requests.exceptions.RequestException as error:
        print('Error fetching order status:', error)

# Example usage
order_status = fetch_order_status(order_id="111111111111")
print(order_status)