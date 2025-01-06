import asyncio
import time
import hmac
import base64
import hashlib
import websockets
import os
import json
import logging
from dotenv import load_dotenv

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

load_dotenv()
api_url = os.getenv('API_URL')
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')


async def get_balance():
    try:
        url = f'wss://{api_url}/v2/websocket'
        async with websockets.connect(url) as ws:
            while True:
                if not ws.open:
                    logger.info("WebSocket disconnected")
                    try:
                        await ws.close()
                    except Exception as e:
                        pass
                    ws = await websockets.connect(url)

                response = await ws.recv()
                data = json.loads(response)
                if 'success' in data and data['success'] is False:
                    logger.warning(data)
                    break

                if 'nonce' in data:
                    ts = str(int(time.time() * 1000))
                    sig_payload = (ts + 'GET/auth/self/verify').encode('utf-8')
                    signature = base64.b64encode(
                        hmac.new(api_secret.encode('utf-8'), sig_payload, hashlib.sha256).digest()).decode('utf-8')
                    auth = {
                        "op": "login",
                        "tag": 1,
                        "data": {
                            "apiKey": api_key,
                            "timestamp": ts,
                            "signature": signature
                        }
                    }
                    await ws.send(json.dumps(auth))
                elif ('table' in data and data['table'] == 'balance') \
                        or ('event' in data and data['event'] == 'login' and 'success' in data and data['success']):
                    logger.info(data)
                    await asyncio.sleep(1)
                    await ws.send(json.dumps({
                        "op": "subscribe",
                        "args": ["balance:all"],
                        "tag": 101
                    }))
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        try:
            await ws.close()
        except Exception as e:
            pass


if __name__ == "__main__":
    try:
        asyncio.run(get_balance())
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
