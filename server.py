from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# App sends -> Relay forwards
@socketio.on("send_data")
def handle_send_data(data):
    client_ip = request.remote_addr
    print(f"Relaying data from {client_ip}")
    socketio.emit("send_data", {"ip": client_ip, "payload": data}, broadcast=True)

@app.route("/")
def index():
    return "Relay server running"

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
