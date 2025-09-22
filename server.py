# server.py
import socketio

# Standard Socket.IO server
sio = socketio.Server(async_mode='threading')
app = socketio.WSGIApp(sio)

# This holds your LAN client connection
lan_client_sid = None

@sio.event
def connect(sid, environ):
    print("Client connected:", sid)

@sio.event
def disconnect(sid):
    global lan_client_sid
    print("Client disconnected:", sid)
    if sid == lan_client_sid:
        lan_client_sid = None

# Event from LAN listener to identify itself
@sio.event
def lan_hello(sid, data):
    global lan_client_sid
    lan_client_sid = sid
    print("LAN listener connected:", sid)

# Event from client apps
@sio.event
def submit(sid, data):
    if lan_client_sid:
        # Relay immediately to your LAN listener
        sio.emit("relay_to_lan", data, room=lan_client_sid)
        print("Relayed data to LAN listener:", data)
    else:
        print("No LAN listener connected, dropping data!")

if __name__ == "__main__":
    import eventlet
    import eventlet.wsgi
    from flask import Flask

    flask_app = Flask(__name__)
    # Mount Socket.IO
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
