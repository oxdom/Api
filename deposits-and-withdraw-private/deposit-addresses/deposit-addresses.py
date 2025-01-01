import os
import requests
import hmac
import hashlib
import base64
from dotenv import load_dotenv
from datetime import datetime
import random
import string

load_dotenv()

def get_deposit_address(asset, network):
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    timestamp = datetime.utcnow().isoformat()
    nonce = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    method = 'GET'
    path = 'api.ox.fun'
    endpoint = '/v3/deposit-addresses'
    query = f'asset={asset}&network={network}'
    msg_string = f'{timestamp}\n{nonce}\n{method}\n{path}\n{endpoint}\n{query}'

    sign = base64.b64encode(hmac.new(secret_key, msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

    try:
        response = requests.get(f'https://{path}{endpoint}?{query}', headers={
            'Content-Type': 'application/json',
            'AccessKey': api_key,
            'Timestamp': timestamp,
            'Signature': sign,
            'Nonce': nonce
        })
        response_data = response.json()
        if response_data.get('success'):
            return response_data['data']['address']
        else:
            print('Failed to fetch deposit address')
    except requests.exceptions.RequestException as error:
        print('Error making API request:', error)

# Example usage

address = get_deposit_address('OX', 'Solana')
print(address)


