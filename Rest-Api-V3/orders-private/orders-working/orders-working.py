import os
import requests
import hmac
import hashlib
import base64
import time
from dotenv import load_dotenv

load_dotenv()

def fetch_working_orders(market_code, order_id=None, client_order_id=None):
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    ts = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    nonce = str(int(time.time() * 1000))
    method = "/v3/orders/working"
    api_url = "api.ox.fun"

    query_string = f"marketCode={market_code}"
    if order_id:
        query_string += f"&orderId={order_id}"
    if client_order_id:
        query_string += f"&clientOrderId={client_order_id}"

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
            print('Failed to fetch working orders')
    except requests.exceptions.RequestException as error:
        print('Error fetching working orders:', error)

# Example usage
orders = fetch_working_orders("BTC-USD-SWAP-LIN", order_id=None, client_order_id=None)
print(orders)