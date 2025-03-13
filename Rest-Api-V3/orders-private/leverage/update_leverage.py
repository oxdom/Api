import os
import requests
import hmac
import hashlib
import base64
import time
from dotenv import load_dotenv

load_dotenv()


def adjust_leverage(market_code, leverage):
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    ts = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    nonce = str(int(time.time() * 1000))
    method = "/v3/leverage"
    api_url = "api.ox.fun"

    payload = {
        "marketCode": market_code,
        "leverage": leverage
    }

    # Convert payload to JSON string
    payload_str = str(payload).replace("'", '"')
    msg_string = f"{ts}\n{nonce}\nPOST\n{api_url}\n{method}\n{payload_str}"

    # Generate HMAC SHA256 signature
    sign = base64.b64encode(hmac.new(secret_key, msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'AccessKey': api_key,
        'Timestamp': ts,
        'Signature': sign,
        'Nonce': nonce
    }

    url = f"https://{api_url}{method}"

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get('success'):
            print('Leverage Adjustment Successful:', data['data'])
        else:
            print('Failed to adjust leverage:', data)
    except requests.exceptions.RequestException as error:
        print('Error adjusting leverage:', error)


# Example usage
market_code = 'BTC-USD-SWAP-LIN'
leverage = 1  # Example leverage value
adjust_leverage(market_code, leverage)
