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

def get_withdrawal_fee(asset, network, address, memo, quantity, external_fee):
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    timestamp = datetime.utcnow().isoformat()
    nonce = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    verb = 'GET'
    path = 'api.ox.fun'
    method = '/v3/withdrawal-fee'
    body = f'asset={asset}&network={network}&address={address}&quantity={quantity}&externalFee={external_fee}'
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

        if response.json().get('success'):
            print('Withdrawal Fee Data:', response.json().get('data'))
        else:
            print('Failed to fetch withdrawal fee data')
    except requests.exceptions.RequestException as error:
        print('Error making API request:', error)

# Example usage
withdrawal_wallet = os.getenv('WITHDRAW_ADDRESS')
if not withdrawal_wallet:
    print('WITHDRAW_ADDRESS environment variable is not set.')
else:
    get_withdrawal_fee('OX', 'Solana', withdrawal_wallet, '', '100.0', True)