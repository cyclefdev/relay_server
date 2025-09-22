import socketio
from flask import Flask, request

# Flask + Socket.IO setup
sio = socketio.Server(cors_allowed_origins="*")
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# Store phone_id -> session mapping
clients = {}

@sio.event
def connect(sid, environ):
    print(f"[+] Phone connected: {sid}")

@sio.event
def register(sid, data):
    """Phone sends its ID when connecting"""
    phone_id = data.get("phone_id")
    if phone_id:
        clients[phone_id] = sid
        print(f"[+] Registered phone_id={phone_id} with sid={sid}")
        sio.emit("registered", {"status": "ok"}, room=sid)

@sio.event
def relay_data(sid, data):
    """Relay incoming phone data to LAN machine"""
    phone_id = data.get("phone_id")
    payload = data.get("payload")

    if not phone_id or not payload:
        return

    print(f"[>] Data from phone {phone_id}: {len(payload)} bytes")

    # Send to all LAN listeners
    sio.emit("store_data", {"phone_id": phone_id, "payload": payload})

@sio.event
def disconnect(sid):
    print(f"[-] Disconnected: {sid}")
    # Remove phone from clients dict
    for phone_id, s in list(clients.items()):
        if s == sid:
            del clients[phone_id]
            print(f"[-] Removed phone_id={phone_id}")


if __name__ == "__main__":
    import eventlet
    import eventlet.wsgi
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    print(f"[*] Starting server on port {port}")
    eventlet.wsgi.server(eventlet.listen(('', port)), app)
