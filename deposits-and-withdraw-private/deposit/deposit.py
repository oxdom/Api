import os
import requests
import hmac
import hashlib
import base64
from dotenv import load_dotenv
from datetime import datetime
import random
import string
import time

load_dotenv()

def get_deposit_data(asset, limit, start_time, end_time):
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    timestamp = datetime.utcnow().isoformat()
    nonce = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    method = 'GET'
    path = 'api.ox.fun'
    endpoint = '/v3/deposit'
    query = f'asset={asset}&limit={limit}&startTime={start_time}&endTime={end_time}'
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
            return response_data['data']
        else:
            print('Failed to fetch deposit data')
    except requests.exceptions.RequestException as error:
        print('Error making API request:', error)

# Example usage
start_time = int(time.time() * 1000) - 24 * 60 * 60 * 1000  # 24 hours ago in milliseconds
end_time = int(time.time() * 1000)  # current time in milliseconds
deposit_data = get_deposit_data('OX', 100, start_time, end_time)
print(deposit_data)
