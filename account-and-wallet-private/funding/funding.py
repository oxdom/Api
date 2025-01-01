import os
import time
import hmac
import hashlib
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_funding_data(market_code, limit=100, start_time=None, end_time=None):
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    ts = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    nonce = str(int(time.time() * 1000))
    method = "/v3/funding"
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
    
    try:
        response = requests.get(f"https://{api_url}{method}?{query_string}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print('Error fetching funding data:', error)

# Example usage
# start time and end time are in milliseconds and must be within 7 days of each other
start_time = int(time.time() * 1000) - 24 * 60 * 60 * 1000  # 24 hours ago in milliseconds
end_time = int(time.time() * 1000)
response = fetch_funding_data('BTC-USD-SWAP-LIN', 100, start_time, end_time)
print(response)