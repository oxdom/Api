import os
import requests
import hmac
import hashlib
import base64
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

def get_account_names():
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    ts = datetime.utcnow().isoformat()
    nonce = str(int(time.time() * 1000))
    method = "/v3/account/names"
    api_url = "api.ox.fun"
    body = ""

    msg_string = f'{ts}\n{nonce}\nGET\n{api_url}\n{method}\n{body}'
    sign = base64.b64encode(hmac.new(secret_key, msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'AccessKey': api_key,
        'Timestamp': ts,
        'Signature': sign,
        'Nonce': nonce
    }

    try:
        url = f'https://{api_url}{method}'
        response = requests.get(url, headers=headers)

        print("Raw Response Content:", response.content)

        if response.headers.get('Content-Type') == 'application/json':
            response_data = response.json()
            if response_data.get('success'):                
                return response_data.get('data')
            else:
                print('Failed to fetch account names')
        else:
            print('Response is not in JSON format')

    except requests.exceptions.RequestException as error:
        print('Error making API request:', error)

# Example usage
response = get_account_names()
print(response)