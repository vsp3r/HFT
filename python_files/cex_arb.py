import asyncio
import websockets
import json
from datetime import datetime
import time

import logging
import threading

import eth_account
import utils
from eth_account.signers.local import LocalAccount

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants
from hyperliquid.utils.signing import get_timestamp_ms
from hyperliquid.utils.types import (
    SIDES,
    Dict,
    L2BookMsg,
    L2BookSubscription,
    Literal,
    Optional,
    Side,
    TypedDict,
    Union,
    UserEventsMsg,
)

InFlightOrder = TypedDict("InFlightOrder", {"type": Literal["in_flight_order"], "time": int})
Resting = TypedDict("Resting", {"type": Literal["resting"], "px": float, "oid": int})
Cancelled = TypedDict("Cancelled", {"type": Literal["cancelled"]})
ProvideState = Union[InFlightOrder, Resting, Cancelled]

BID_DIFF_THRESHOLD = 0.00007  # Example value, adjust based on your analysis
ASK_DIFF_THRESHOLD = 0.00007  # Example value, adjust based on your analysis
TRADE_COOLDOWN = 5  # in seconds, to prevent rapid trades
MAX_POSITION = 1000 # all of these values should be adjusted based on coin
COIN = 'GMT'

def side_to_int(side: Side) -> int: #could perhaps replace with enums like order types in rtg
    return 1 if side == "A" else -1


def side_to_uint(side: Side) -> int:
    return 1 if side == "A" else 0

class AutoTrader:
    def __init__(self, wallet: LocalAccount, api_url: str, coin: str):
        self.info = Info(api_url)
        self.exchange = Exchange(wallet, api_url)
        self.exchange.update_leverage(50, coin)
        self.coin = coin
        self.position: Optional[float] = None

        self.binance_bbo = {}
        self.hyperliquid_bbo = {}
        self.last_trade_time = None

    def run(self):
        loop = asyncio.get_event_loop()
        tasks = [self.connect_binance(), self.connect_hyperliquid()]
        loop.run_until_complete(asyncio.gather(*tasks))

    async def connect_binance(self):
        uri = 'wss://fstream.binance.com/ws'  
        async with websockets.connect(uri) as websocket:
            c = self.coin.lower() + 'usdt'
            level = 5
            speed = 0
            stream = f'{c}@depth{level}@{speed}ms'
            stream = [stream]

            subscription_message = {
                "method":"SUBSCRIBE",
                "params":stream,
                'id':1
            }
            await websocket.send(json.dumps(subscription_message))

            m = 0
            msg = await websocket.recv()
            while True:
                m += 1
                message = await websocket.recv()
                # print(f'BINANCE({m}): {message}')
                self.handle_binance(json.loads(message), m)

    async def connect_hyperliquid(self):
        uri = "wss://api.hyperliquid.xyz/ws"  
        # uri = 'wss://api.hyperliquid-testnet.xyz/ws'   

        async with websockets.connect(uri) as websocket:
            subscription_message = {
                "method": "subscribe",
                "subscription": { "type": "l2Book", "coin": self.coin }
                # Add any additional fields specific to your subscription message
            }
            
            await websocket.send(json.dumps(subscription_message))
            n = 0
            msg = await websocket.recv()
            msg2 = await websocket.recv()
            while True:
                message = await websocket.recv()
                n += 1
                # print(f'HYPERLIQUID({n}): {message}')
                self.handle_hyperliquid(json.loads(message), n)

    def handle_binance(self, message, msg_num):
        self.binance_bbo['bid'] = float(message['b'][0][0])
        self.binance_bbo['ask'] = float(message['a'][0][0])
        self.binance_bbo['ts'] = int(message['E'])
        print(f'Binance ({msg_num}): Bid: {self.binance_bbo["bid"]}, Ask: {self.binance_bbo["ask"]}')
        self.compute_differences_and_trade()

    def handle_hyperliquid(self, message, msg_num):
        self.hyperliquid_bbo['bid'] = float(message['data']['levels'][0][0]['px'])
        self.hyperliquid_bbo['ask'] = float(message['data']['levels'][1][0]['px'])
        self.hyperliquid_bbo['ts'] = int(message['data']['time'])
        print(f'Hyperliquid ({msg_num}): Bid: {self.hyperliquid_bbo["bid"]}, Ask: {self.hyperliquid_bbo["ask"]}')

    def compute_differences_and_trade(self):
        current_time = get_timestamp_ms()
        if not self.binance_bbo or not self.hyperliquid_bbo:
            return
        
        bid_diff = self.binance_bbo['bid'] - self.hyperliquid_bbo['bid'] - self.diff
        ask_diff = self.binance_bbo['ask'] - self.hyperliquid_bbo['ask'] - self.diff

        # bull case:
        # binance: bid 1.6123 -> 1.6127 (+0.0004)
        # hl: bid 1.6120 -> 1.6124 (+ 0.0004)
        # bear case:
        # binance: bid 1.6127 -> 1.6123 (-0.0004)
        # hl: bid 1.6124 -> 1.6120 ()
        # Check if the differences exceed thresholds
        if (abs(bid_diff) > BID_DIFF_THRESHOLD or abs(ask_diff) > ASK_DIFF_THRESHOLD) and \
                (not last_trade_time or (current_time - last_trade_time) > TRADE_COOLDOWN):
            # Place your trade logic here
            self.place_trade(bid_diff, ask_diff)
            last_trade_time = current_time
    def place_trade(self, bid_diff, ask_diff):
        sz = MAX_POSITION
        side = bid_diff > 0
        ideal_price = self.hyperliquid_bbo['ask'] + bid_diff if side else self.hyperliquid_bbo['bid'] + ask_diff
        px = float(f"{ideal_price:.5g}")
        print(f"PLACING ORDER sz:{sz} px:{px} side:{side}")
        response = self.exchange.order(self.coin, side, sz, px, {'limit':{'tif':'Gtc'}})
        print(f'PLACED ORDER {response}')





# # Global variables to store BBO data
# binance_bbo = {}
# hyperliquid_bbo = {}
# last_trade_time = None

# Constants (can be adjusted based on your strategy)

# def compute_differences_and_trade():
#     global last_trade_time
#     current_time = int(time.time() * 1000)

#     if not binance_bbo or not hyperliquid_bbo:
#         return

#     bid_diff = binance_bbo['bid'] - hyperliquid_bbo['bid']
#     ask_diff = binance_bbo['ask'] - hyperliquid_bbo['ask']

#     # Check if the differences exceed thresholds
#     if (abs(bid_diff) > BID_DIFF_THRESHOLD or abs(ask_diff) > ASK_DIFF_THRESHOLD) and \
#             (not last_trade_time or (current_time - last_trade_time) > TRADE_COOLDOWN):
#         # Place your trade logic here
#         place_trade(bid_diff, ask_diff)
#         last_trade_time = current_time

# def place_trade(bid_diff, ask_diff):
#     # Implement your trade logic here
#     if bid_diff > BID_DIFF_THRESHOLD:
#         # Example: Buy on Hyperliquid, Sell on Binance
#         print(f"Trading opportunity detected! Bid difference: {bid_diff}")
#     elif ask_diff > ASK_DIFF_THRESHOLD:
#         # Example: Sell on Hyperliquid, Buy on Binance
#         print(f"Trading opportunity detected! Ask difference: {ask_diff}")


def main():
    logging.basicConfig(level=logging.ERROR)
    config = utils.get_config()
    account = eth_account.Account.from_key(config["secret_key"])
    print("Running with account address:", account.address)
    trader = AutoTrader(account, constants.TESTNET_API_URL, coin=COIN)
    trader.run()


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # tasks = [connect_binance(), connect_hyperliquid()]
    # loop.run_until_complete(asyncio.gather(*tasks))
    main()



### Trading Logic


### Binance Stream


### Hyperliquid Stream


