import socketio
from flask import Flask

app = Flask(__name__)
sio = socketio.Server(cors_allowed_origins="*")
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# Relay incoming data directly to all connected clients (like your Linux box)
@sio.event
def send_data(sid, data):
    try:
        device_id = data.get("device_id")
        payload = data.get("payload")

        if not device_id or not payload:
            print("[!] Missing device_id or payload")
            return

        print(f"[Relay] From device {device_id}: {payload}")

        # Relay to all connected listeners except the sender
        sio.emit("forward_data", data, skip_sid=sid)

    except Exception as e:
        print(f"[!] Relay error: {e}")

@sio.event
def connect(sid, environ):
    print(f"[+] Client connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"[-] Client disconnected: {sid}")

if __name__ == "__main__":
    import eventlet
    import eventlet.wsgi
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 5000)), app)
