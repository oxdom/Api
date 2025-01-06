import asyncio
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


async def get_trade(market_code):
    try:
        async with websockets.connect(f"wss://{api_url}/v2/websocket") as websocket:
            while True:
                if not websocket.open:
                    logger.info("websocket disconnected")
                    try:
                        await websocket.close()
                    except Exception as e:
                        pass
                    websocket = await websockets.connect(f"wss://{api_url}/v2/websocket")
                response = await websocket.recv()
                res = json.loads(response)
                if 'success' in res and res['success'] is False:
                    logger.warning(res)
                    break

                if 'nonce' in res:
                    await websocket.send(json.dumps({
                        "op": "subscribe",
                        "tag": 1,
                        "args": [f"trade:{market_code}"]
                    }))
                if 'data' in res:
                    logger.info(res['data'])
                    await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        try:
            await websocket.close()
        except Exception as e:
            pass


if __name__ == "__main__":
    try:
        asyncio.run(get_trade("BTC-USD-SWAP-LIN"))
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
