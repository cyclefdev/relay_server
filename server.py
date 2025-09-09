from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

clients = []

# Device connects via WebSocket
@socketio.on("connect")
def handle_connect():
    clients.append(request.sid)
    print(f"Device connected: {request.sid}")

# Device disconnects
@socketio.on("disconnect")
def handle_disconnect():
    if request.sid in clients:
        clients.remove(request.sid)
    print(f"Device disconnected: {request.sid}")

# Phones send data via POST
@app.route("/submit", methods=["POST"])
def submit():
    data = request.form.to_dict() or request.json
    print("Got data from phone:", data)
    # Forward to all connected devices
    for sid in clients:
        socketio.emit("data_from_app", data, to=sid)
    return "Forwarded", 200

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
