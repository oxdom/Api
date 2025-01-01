import os
import requests
import hmac
import hashlib
import base64
import time
from dotenv import load_dotenv

load_dotenv()
def fetch_positions(sub_accounts, market_code):
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    ts = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    nonce = str(int(time.time() * 1000))
    method = "/v3/positions"
    api_url = "api.ox.fun"
    
    sub_acc_param = f"subAcc={','.join(sub_accounts)}" if sub_accounts else ""
    query_string = f"{sub_acc_param}&marketCode={market_code}".strip('&')
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
        print('Error fetching positions:', error)
# Example usage
# Example usage
sub_accounts = None
market_code = 'BTC-USD-SWAP-LIN'
response = fetch_positions(sub_accounts, market_code)
print(response)