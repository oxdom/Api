import os
import datetime
import time
import json
import base64
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

def make_withdrawal():
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('API_SECRET').encode('utf-8')
    withdraw_address = os.getenv('WITHDRAW_ADDRESS')
    ts = datetime.datetime.utcnow().isoformat()
    nonce = str(int(time.time() * 1000))
    method = "/v3/withdrawal"
    api_url = "api.ox.fun"
    timestamp = int(round(time.time() * 1000))
    post_data = {
        "asset": "OX",
        "network": "Solana",
        "address": withdraw_address,
        "quantity": "100",
        "externalFee": True,
        "recvWindow": 3000,
        "timestamp": timestamp,
        "responseType": "FULL"
    }
    body = json.dumps(post_data)

    msg_string = '{}\n{}\n{}\n{}\n{}\n{}'.format(ts, nonce, 'POST', api_url, method, body)
    sig = base64.b64encode(hmac.new(secret_key, msg_string.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'AccessKey': api_key,
        'Timestamp': ts,
        'Signature': sig,
        'Nonce': nonce
    }

    try:
        response = requests.post(f"https://{api_url}{method}", data=body, headers=headers)
        print("Status Code:", response.status_code)
        print("Response Text:", response.json())  # Print the raw response content
    except requests.exceptions.RequestException as e:
        print('Error making withdrawal request:', e)

make_withdrawal()