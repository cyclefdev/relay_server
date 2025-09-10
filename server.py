from flask import Flask, request
from flask_socketio import SocketIO, emit
import base64

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

@app.route("/submit", methods=["POST"])
def submit():
    phone_id = request.form.get("phone_id")
    if not phone_id:
        return "Phone ID is required", 400

    # Forward form data
    data = {k: v for k, v in request.form.items() if k != "media"}
    socketio.emit("data_from_app", {"phone_id": phone_id, "data": data})

    # Forward file if present
    if "media" in request.files:
        file = request.files["media"]
        filename = f"{phone_id}_{file.filename}"
        file_data = file.read()

        # Encode file as base64 string for safe transport
        b64_data = base64.b64encode(file_data).decode("utf-8")

        socketio.emit("file_from_app", {"phone_id": phone_id, "filename": filename, "data": b64_data})

    return "Data forwarded", 200

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
