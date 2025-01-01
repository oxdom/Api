import os
import datetime
import time
import base64
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()



def get_withdrawal(id, asset, limit, start_time, end_time):
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    timestamp = datetime.datetime.utcnow().isoformat()
    nonce = str(int(time.time() * 1000))
    verb = 'GET'
    path = 'api.ox.fun'
    method = '/v3/withdrawal'
    body = f'id={id}&asset={asset}&limit={limit}&startTime={start_time}&endTime={end_time}'    
    msg_string = f'{timestamp}\n{nonce}\n{verb}\n{path}\n{method}\n{body}'
    sign = base64.b64encode(hmac.new(secret_key, msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')
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
            return response_data
        else:
            print('Failed to fetch withdrawal data', response_data)
    except requests.exceptions.RequestException as error:
        print('Error making API request:', error)
        
        
# Ensure start_time and end_time are within 7 days of each other
current_time = int(time.time() * 1000)
seven_days_ago = current_time - (7 * 24 * 60 * 60 * 1000)

response = get_withdrawal('11111111111111111', 'OX', 100, seven_days_ago, current_time)
print(response)
