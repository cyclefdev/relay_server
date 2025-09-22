# server.py
import asyncio
import websockets
import json

clients = set()  # Connected Linux clients

async def handler(websocket, path):
    # Expect Linux device to identify itself with "type":"receiver"
    data = await websocket.recv()
    try:
        message = json.loads(data)
    except:
        return

    if message.get("type") == "receiver":
        clients.add(websocket)
        print("Receiver connected")
    else:
        # Forward message to all receivers
        disconnected = []
        for client in clients:
            try:
                await client.send(data)
            except:
                disconnected.append(client)
        for d in disconnected:
            clients.remove(d)

    try:
        async for message in websocket:
            pass
    finally:
        if websocket in clients:
            clients.remove(websocket)
            print("Receiver disconnected")

start_server = websockets.serve(handler, "0.0.0.0", 8765)
print("Relay server started on port 8765")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
