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


class ConnectionPool:
    def __init__(self, max_connections):
        self.max_connections = max_connections
        self.connections = []
        self.semaphore = asyncio.Semaphore(max_connections)

    async def acquire(self):
        async with self.semaphore:
            logger.info(f"Connection pool size: {len(self.connections)}")
            if len(self.connections) < int(self.max_connections):
                ws = await websockets.connect(f"wss://{api_url}/v2/websocket")
                self.connections.append(ws)
                return ws
            else:
                raise Exception("Connection pool limit reached")

    async def release(self, ws):
        await ws.close()
        self.connections.remove(ws)


connection_pool = ConnectionPool(5)


class WebSocketClient:
    def __init__(self, input_market_code):
        self.CHECK_BUFFER_INTERVAL = 0.02
        self.PLACE_BUFFER_INTERVAL = 0.03

        self.market_code = input_market_code

        self.mark_price = -1.0
        self.min_qty = 0.0
        self.tick_size = 0.0

        self.bids_len = 0
        self.asks_len = 0
        self.best_bid_price = -1.0
        self.best_ask_price = -1.0
        self.worst_bid_price = -1.0
        self.worst_ask_price = -1.0

        self.upper_price_bound = -1.0
        self.lower_price_bound = -1.0

    async def get_mark_price(self):
        try:
            websocket = await connection_pool.acquire()
            while True:
                if not websocket.open:
                    try:
                        await connection_pool.release(websocket)
                    except Exception as e:
                        pass
                    websocket = await connection_pool.acquire()
                response = await websocket.recv()
                res = json.loads(response)

                if 'nonce' in res:
                    await websocket.send(json.dumps({
                        "op": "subscribe",
                        "tag": 1,
                        "args": [f"market:{self.market_code}"]
                    }))
                if 'data' in res and len(res['data']) > 0:
                    mark_price = float(res['data'][0]['marketPrice'])
                    min_qty = float(res['data'][0]['qtyIncrement'])
                    tick_size = float(res['data'][0]['tickSize'])
                    upper_price_bound = float(res['data'][0]['upperPriceBound'])
                    lower_price_bound = float(res['data'][0]['lowerPriceBound'])
                    setattr(self, 'mark_price', mark_price)
                    setattr(self, 'min_qty', min_qty)
                    setattr(self, 'tick_size', tick_size)
                    setattr(self, 'upper_price_bound', upper_price_bound)
                    setattr(self, 'lower_price_bound', lower_price_bound)

                    # logger.info(f"[x] get_mark_price - {res['data']}")
                    await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Error in get_mark_price: {e}")
            try:
                await connection_pool.release(websocket)
            except Exception as e:
                pass

    async def get_order_book_info(self):
        try:
            websocket = await connection_pool.acquire()
            while True:
                if not websocket.open:
                    try:
                        await connection_pool.release(websocket)
                    except Exception as e:
                        pass
                    websocket = await connection_pool.acquire()
                response = await websocket.recv()
                res = json.loads(response)

                if 'nonce' in res:
                    await websocket.send(json.dumps({
                        "op": "subscribe",
                        "tag": 103,
                        "args": [f"depthL25:{self.market_code}"]
                    }))
                if 'data' in res:
                    if 'asks' in res['data']:
                        asks_list = res['data']['asks']
                        asks_len = len(asks_list)
                        setattr(self, 'asks_len', asks_len)
                        if asks_len > 0:
                            best_ask_price = asks_list[0][0]
                            worst_ask_price = asks_list[-1][0]
                            setattr(self, 'best_ask_price', best_ask_price)
                            setattr(self, 'worst_ask_price', worst_ask_price)
                        else:
                            setattr(self, 'best_ask_price', -1)
                            setattr(self, 'worst_ask_price', -1)
                    if 'bids' in res['data']:
                        bids_list = res['data']['bids']
                        bids_len = len(res['data']['bids'])
                        setattr(self, 'bids_len', bids_len)
                        if bids_len > 0:
                            best_bid_price = bids_list[0][0]
                            worst_bid_price = bids_list[-1][0]
                            setattr(self, 'best_bid_price', best_bid_price)
                            setattr(self, 'worst_bid_price', worst_bid_price)
                        else:
                            setattr(self, 'best_bid_price', -1)
                            setattr(self, 'worst_bid_price', -1)

                    # logger.info(f"[x] get_order_book_info - {res['data']}")
                    await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Error in get_order_book_info: {e}")
            try:
                await connection_pool.release(websocket)
            except Exception as e:
                pass

    async def verify_place_modify_cancel_bid_order(self):
        try:
            ws = await connection_pool.acquire()
            while True:
                if not ws.open:
                    try:
                        await connection_pool.release(ws)
                    except Exception as e:
                        pass
                    ws = await connection_pool.acquire()

                response = await ws.recv()
                data = json.loads(response)

                if 'nonce' in data:
                    ts = str(int(time.time() * 1000))
                    sig_payload = (ts + 'GET/auth/self/verify').encode('utf-8')
                    signature = base64.b64encode(
                        hmac.new(api_secret.encode('utf-8'), sig_payload, hashlib.sha256).digest()).decode(
                        'utf-8')
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
                elif 'event' in data \
                        and ((
                                     data['event'] == 'cancelorder'
                                     and 'data' in data and 'clientOrderId' in data['data']
                                     and int(data['data']['clientOrderId']) == 1
                                     and 'marketCode' in data['data'] and data['data'][
                                         'marketCode'] == self.market_code
                             )
                             or (data['event'] == 'login' and 'success' in data and data['success'])):
                    if 'event' in data \
                            and (
                            data['event'] == 'cancelorder'
                            and 'marketCode' in data['data'] and data['data'][
                                'marketCode'] == self.market_code
                    ):
                        logger.info(
                            f"[x] (cancelorder) - {data}")

                    while self.mark_price == -1.0 or self.min_qty == 0.0:
                        await asyncio.sleep(1)

                    # verification
                    if (self.bids_len < 10 or self.best_bid_price < self.mark_price * (
                            1 - self.CHECK_BUFFER_INTERVAL) or self.best_bid_price == -1.0) \
                            or \
                            (self.asks_len < 10 or self.best_ask_price > self.mark_price * (
                                    1 + self.CHECK_BUFFER_INTERVAL) or self.best_ask_price == -1.0):
                        if self.bids_len > 0 and self.worst_bid_price != -1:
                            if self.worst_bid_price > self.tick_size:
                                order_price = self.worst_bid_price * (1 - self.PLACE_BUFFER_INTERVAL)
                            else:
                                order_price = self.worst_bid_price
                        else:
                            if self.best_ask_price != -1 and self.best_ask_price < self.mark_price:
                                order_price = self.best_ask_price * (1 - self.PLACE_BUFFER_INTERVAL)
                            else:
                                order_price = self.mark_price * (1 - self.PLACE_BUFFER_INTERVAL)

                        if self.upper_price_bound != -1 and self.lower_price_bound != -1:
                            if order_price < self.lower_price_bound \
                                    and self.lower_price_bound + self.tick_size < self.best_ask_price:
                                order_price = self.lower_price_bound + self.tick_size
                            elif order_price > self.upper_price_bound \
                                    and self.upper_price_bound - self.tick_size < self.best_ask_price:
                                order_price = self.upper_price_bound - self.tick_size

                        await ws.send(json.dumps({
                            "op": "placeorder",
                            "tag": 123,
                            "data": {
                                "clientOrderId": 1,
                                "marketCode": self.market_code,
                                "side": "BUY",
                                "orderType": "LIMIT",
                                "quantity": self.min_qty,
                                "price": order_price
                            }
                        }))
                        await asyncio.sleep(1)
                elif 'event' in data \
                        and (
                        data['event'] == 'placeorder'
                        and 'data' in data and 'clientOrderId' in data['data']
                        and int(data['data']['clientOrderId']) == 1
                        and 'marketCode' in data['data'] and data['data'][
                            'marketCode'] == self.market_code
                        and 'BUY' in data['data']['side']
                ):
                    logger.info(f"[x] (placeorder) - {data}")
                    await ws.send(json.dumps({
                        "op": "modifyorder",
                        "tag": 1,
                        "data": {
                            "marketCode": self.market_code,
                            "orderId": int(data['data']['orderId']),
                            "side": "BUY",
                            "price": float(data['data']['limitPrice']),
                            "quantity": self.min_qty * 2
                        }
                    }))
                    await asyncio.sleep(1)
                elif 'event' in data \
                        and (
                        data['event'] == 'modifyorder'
                        and 'data' in data and 'clientOrderId' in data['data']
                        and int(data['data']['clientOrderId']) == 1
                        and 'marketCode' in data['data'] and data['data'][
                            'marketCode'] == self.market_code
                ):
                    logger.info(f"[x] (modifyorder) - {data}")
                    await ws.send(json.dumps({
                        "op": "cancelorder",
                        "tag": 456,
                        "data": {
                            "marketCode": self.market_code,
                            "orderId": int(data['data']['orderId']),
                        }
                    }))
                    await asyncio.sleep(1)
                    continue
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            try:
                await connection_pool.release(ws)
            except Exception as e:
                pass

    async def run(self):
        # Run all tasks concurrently
        await asyncio.gather(
            self.get_mark_price(),
            self.get_order_book_info(),
            self.verify_place_modify_cancel_bid_order(),
        )


if __name__ == "__main__":
    try:
        client = WebSocketClient("HYPE-USD-SWAP-LIN")
        asyncio.run(client.run())
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
