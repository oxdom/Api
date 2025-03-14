import os
import requests
import hmac
import hashlib
import base64
import time
from dotenv import load_dotenv

load_dotenv()

def fetch_trades(market_code, limit, start_time, end_time):
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    ts = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    nonce = str(int(time.time() * 1000))
    method = "/v3/trades"
    api_url = "api.ox.fun"

    query_string = f"marketCode={market_code}&limit={limit}&startTime={start_time}&endTime={end_time}"
    msg_string = f"{ts}\n{nonce}\nGET\n{api_url}\n{method}\n{query_string}"

    sign = base64.b64encode(hmac.new(secret_key, msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'AccessKey': api_key,
        'Timestamp': ts,
        'Signature': sign,
        'Nonce': nonce
    }

    url = f"https://{api_url}{method}?{query_string}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get('success'):
            print('Trades Data:', data['data'])
        else:
            print('Failed to fetch trades')
    except requests.exceptions.RequestException as error:
        print('Error fetching trades:', error)

# Example usage
market_code = 'BTC-USD-SWAP-LIN'
limit = 100
start_time = int(time.time() * 1000) - 24 * 60 * 60 * 1000  # 24 hours ago
end_time = int(time.time() * 1000)
fetch_trades(market_code, limit, start_time, end_time)