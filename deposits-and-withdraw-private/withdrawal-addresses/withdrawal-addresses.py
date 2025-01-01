import os
import datetime
import time
import base64
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

def get_withdrawal_address(asset, network):
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    timestamp = datetime.datetime.utcnow().isoformat()
    nonce = str(int(time.time() * 1000))
    verb = 'GET'
    path = 'api.ox.fun'
    method = '/v3/withdrawal-addresses'
    body = f'asset={asset}&network={network}'

    msg_string = f'{timestamp}\n{nonce}\n{verb}\n{path}\n{method}\n{body}'
    sign = base64.b64encode(hmac.new(secret_key, msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

    try:
        response = requests.get(f'https://{path}{method}?{body}', headers={
            'Content-Type': 'application/json',
            'AccessKey': api_key,
            'Timestamp': timestamp,
            'Signature': sign,
            'Nonce': nonce
        })
        response_data = response.json()
        if response_data.get('success'):
            print('Withdrawal Address:', response_data['data'])
        else:
            print('Failed to fetch withdrawal address')
    except requests.exceptions.RequestException as error:
        print('Error making API request:', error)

# Example usage
get_withdrawal_address('OX', 'Solana')
