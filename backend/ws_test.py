import asyncio
import websockets

async def handler(websocket):
    print("WS CONNECTED")
    i = 0
    while True:
        await websocket.send(f"tick {i}")
        i += 1
        await asyncio.sleep(1)

async def main():
    async with websockets.serve(handler, "127.0.0.1", 8765):
        print("WS server running on 8765")
        await asyncio.Future()

asyncio.run(main())
