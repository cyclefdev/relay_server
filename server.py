import socketio

LAN_SERVER = "http://10.0.2.15:6000"  # replace with your LAN IP

# Socket.IO server for clients
sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

# Socket.IO client to LAN
lan_sio = socketio.Client()
lan_sio.connect(LAN_SERVER)

print("Relay connected to LAN server")

@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.on("client_data")
def handle_client_data(sid, data):
    """
    Receives data from external clients and forwards to LAN server.
    """
    print(f"Relaying data from {sid} to LAN")
    lan_sio.emit("client_data", data)
    sio.emit("ack", {"status": "relayed"}, room=sid)

if __name__ == "__main__":
    import eventlet
    import eventlet.wsgi
    from flask import Flask

    print("Relay server running on 0.0.0.0:5000")
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
