# server.py
from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Connected LAN clients (Linux machines)
lan_clients = []

@app.route("/submit", methods=["POST"])
def submit_data():
    data = request.form.to_dict(flat=False)
    # Forward to all connected LAN clients
    for client in lan_clients:
        client.emit("new_data", data)
    return {"status": "ok"}, 200

@socketio.on("connect")
def handle_connect():
    print(f"LAN client connected: {request.sid}")
    lan_clients.append(socketio)

@socketio.on("disconnect")
def handle_disconnect():
    print(f"LAN client disconnected: {request.sid}")
    if socketio in lan_clients:
        lan_clients.remove(socketio)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
