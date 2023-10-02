import asyncio
import websockets
import json
from datetime import datetime

## BINANCE VERSION
async def connect_to_stream():
    # uri = "wss://fstream.binance.com/ws"  # Replace with the WebSocket stream URL
    uri = 'wss://fstream.binance.com/ws'   
    
    async with websockets.connect(uri) as websocket:
        n = 0
        symbol = 'ethusdt'
        level = 20
        speed = 0
        # stream = "{}@depth{}@{}ms".format(symbol.lower(), level, speed)
        s2 = "ethusdt@depth@100ms"
        stream = [s2]

        subscription_message = {
            "method": "SUBSCRIBE",
            "params": stream,
            'id':1 # Replace with the actual stream name
            # Add any additional fields specific to your subscription message
        }
        
        await websocket.send(json.dumps(subscription_message))
        

        while True:
            message = await websocket.recv()
            n += 1
            print(f'Recieved message ({n}): {message}')
        # Process the received message as per  your requirements
#             if unsubscription_task.done():
#                 break   
# # Run the connection functionee
#                 # Wait for the unsubscription task to complete before closing the connection
            # await send_unsubscription()
        
        # Optionally, you can perform any cle
        # anup or additional tasks here
            # await websocket.close()



async def send_unsubscription(websocket):
    await asyncio.sleep(10)  # Delay before sending the unsubscription message

    symbol = 'ethusdt'
    level = 20
    speed = 0
    stream = "{}@depth{}@{}ms".format(symbol.lower(), level, speed)

    s2 = "ethusdt@depth@100ms"
    stream = [stream]
    unsubscription_message = {
        "method": "UNSUBSCRIBE",
        "stream_name": stream  # Replace with the actual stream name
        # Add any additional fields specific to your unsubscription message
    }

        # json_msg2 = json.dumps({"method": "UNSUBSCRIBE", "params": stream2, "id": id})

    await websocket.send(json.dumps(unsubscription_message))

asyncio.get_event_loop().run_until_complete(connect_to_stream())
