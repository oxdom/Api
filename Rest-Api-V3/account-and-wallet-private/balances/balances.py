import os
import requests
import hmac
import hashlib
import base64
import time
from dotenv import load_dotenv

load_dotenv()

def get_balances(sub_accounts=None, asset=''):
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    ts = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    nonce = str(int(time.time() * 1000))
    method = "/v3/balances"
    api_url = "api.ox.fun"

    # Construct query parameters
    sub_acc_param = f"subAcc={','.join(sub_accounts)}" if sub_accounts else ""
    asset_param = f"asset={asset}" if asset else ""
    query_string = '&'.join(filter(None, [sub_acc_param, asset_param]))

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
        print('Response:', data)

        # Display each account's balances
        for account in data.get('data', []):
            print(f"Account Name: {account['name']}")
            for balance in account['balances']:
                print(f"Asset: {balance['asset']}, Total: {balance['total']}, Available: {balance['available']}, Reserved: {balance['reserved']}")
    except requests.exceptions.RequestException as error:
        print('Error fetching balances:', error)

# Example usage
sub_accounts = ['subaccount1']
asset = 'OX'
get_balances(sub_accounts, asset) 