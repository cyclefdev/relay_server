from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Track connected Linux clients (storage nodes)
linux_clients = set()

@app.route("/")
def index():
    return "Relay server is running."

@socketio.on("connect")
def handle_connect():
    client_ip = request.remote_addr
    print(f"[+] Client connected: {client_ip}")

@socketio.on("disconnect")
def handle_disconnect():
    client_ip = request.remote_addr
    print(f"[-] Client disconnected: {client_ip}")
    if request.sid in linux_clients:
        linux_clients.remove(request.sid)

@socketio.on("register_linux")
def register_linux():
    """Linux storage node registers itself here."""
    linux_clients.add(request.sid)
    print(f"[+] Linux client registered: {request.sid}")

@socketio.on("phone_data")
def handle_phone_data(data):
    """Forward phone data to all Linux storage nodes."""
    client_ip = request.remote_addr
    print(f"[📱] Received data from phone {client_ip} -> forwarding to Linux nodes...")

    if not linux_clients:
        print("[⚠️] No Linux clients connected! Data not stored.")
        return

    for sid in linux_clients:
        socketio.emit("store_data", {"ip": client_ip, "payload": data}, room=sid)
        print(f"[➡️] Forwarded data from {client_ip} to Linux client {sid}")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
