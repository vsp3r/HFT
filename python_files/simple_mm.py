import time 
import json
import asyncio
import threading
from os.path import getmtime
import websockets
import utils
import threading
# import eth_account
# from eth_account.signers.local import LocalAccount

CONFIG_FILE = 'config.json'

class AutoTrader:
    def __init__(self, coin):
        self.binance_book = {}
        self.hyperliquid_book = {}
        self.coin = coin

        self.last_mtime = None
        self.load_config()
        # self.check_config()

    async def run(self):
        threading.Thread(target=self.check_for_config_updates, daemon=True).start()
        await asyncio.gather(self.binance_feed(), self.hyperliquid_feed())

    async def binance_feed(self):
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

    async def hyperliquid_feed(self):
        # uri = "wss://api.hyperliquid.xyz/ws"  
        uri = 'wss://api.hyperliquid-testnet.xyz/ws'   

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
        self.binance_book['bid'] = float(message['b'][0][0])
        self.binance_book['ask'] = float(message['a'][0][0])
        self.binance_book['ts'] = int(message['E'])
        print(f'Binance ({msg_num}): Bid: {self.binance_book["bid"]}, Ask: {self.binance_book["ask"]}')
        # print(f'Binance ({msg_num}): {message}')
        self.compute_trades()

    def handle_hyperliquid(self, message, msg_num):
        self.hyperliquid_book['bid'] = float(message['data']['levels'][0][0]['px'])
        self.hyperliquid_book['ask'] = float(message['data']['levels'][1][0]['px'])
        self.hyperliquid_book['ts'] = int(message['data']['time'])
        print(f'Hyperliquid ({msg_num}): Bid: {self.hyperliquid_book["bid"]}, Ask: {self.hyperliquid_book["ask"]}')
        # print(f'hyperliquid({msg_num}): {message}')


    def compute_trades(self):
        # x = 0
        print(f'Max_pos: {self.max_pos}')

    # def load_config(self):
    #     with open (CONFIG_FILE, 'r') as f:
    #         f = json.load(f)
    #         for key, value in f.items():
    #             if isinstance(value, dict):
    #                 for sub_key, sub_value in value.items():
    #                     setattr(self, sub_key, sub_value)
    #             else:
    #                 setattr(self, key, value)
    #         self.last_mtime = getmtime(CONFIG_FILE)
    def load_config(self):
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            self.max_pos = data['max_pos']
            # ... load other parameters ...
            self.last_mtime = getmtime(CONFIG_FILE)
    
    def check_config(self):
        print(self.__dict__)

    def check_for_config_updates(self):
        while True:
            current_mtime = getmtime(CONFIG_FILE)
            if current_mtime != self.last_mtime:
                self.load_config()
                print("Configuration reloaded!")
            # time.sleep(5)


def get_timestamp_ms() -> int:
    return int(time.time() * 1000)

def main():
    # config = utils.get_config()
    # account = eth_account.Account.from_key(config["secret_key"])
    # print("Running with account address:", account.address)
    trader = AutoTrader('GMT')
    asyncio.run(trader.run())

if __name__ == "__main__":
    main()
