import time
import json
import asyncio
import threading
from os.path import getmtime
# import websockets

CONFIG_FILE = 'config.json'

class TradingBot:

    def __init__(self):
        self.last_mtime = None
        self.load_config()

    def load_config(self):
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            self.max_pos = data['max_pos']
            # ... load other parameters ...
            self.last_mtime = getmtime(CONFIG_FILE)

    def check_for_config_updates(self):
        while True:
            current_mtime = getmtime(CONFIG_FILE)
            if current_mtime != self.last_mtime:
                self.load_config()
                print("Configuration reloaded!")
            # time.sleep(5)

    async def handle_websocket_feed_1(self):
        while True:
            # e.g., async with websockets.connect('ws://example.com/feed1') as ws:
            #          data = await ws.recv()
            print(f"{time.time() * 1000:.3f} - Feed 1 with max_pos: {self.max_pos}")
            await asyncio.sleep(0)

    async def handle_websocket_feed_2(self):
        while True:
            # e.g., async with websockets.connect('ws://example.com/feed2') as ws:
            #          data = await ws.recv()
            print(f"{time.time() * 1000:.3f} - Feed 2 with max_pos: {self.max_pos}")
            await asyncio.sleep(0)

    async def run(self):
        threading.Thread(target=self.check_for_config_updates, daemon=True).start()

        # Here, both WebSocket feed handlers are started concurrently.
        await asyncio.gather(self.handle_websocket_feed_1(), self.handle_websocket_feed_2())

if __name__ == '__main__':
    bot = TradingBot()
    asyncio.run(bot.run())
