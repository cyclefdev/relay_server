from flask import Flask, request
from flask_socketio import SocketIO
import base64
import os

# Initialize Flask + SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Keep track of connected Linux clients
linux_clients = []

# Handle WebSocket connections from Linux client(s)
@socketio.on("connect")
def on_connect():
    linux_clients.append(request.sid)
    print(f"Linux connected: {request.sid}")

@socketio.on("disconnect")
def on_disconnect():
    if request.sid in linux_clients:
        linux_clients.remove(request.sid)
    print(f"Linux disconnected: {request.sid}")

# HTTP endpoint where Android app POSTs data
@app.route("/submit", methods=["POST"])
def submit():
    phone_id = request.form.get("phone_id")
    if not phone_id:
        return "Missing phone_id", 400

    # Extract metadata except the file
    data = {k: v for k, v in request.form.items() if k != "media"}

    # Forward metadata to Linux client(s)
    for client in linux_clients:
        socketio.emit("data_from_app", {"phone_id": phone_id, "data": data}, to=client)

    # Forward file (if any) to Linux client(s)
    if "media" in request.files:
        file = request.files["media"]
        b64_data = base64.b64encode(file.read()).decode("utf-8")
        for client in linux_clients:
            socketio.emit("file_from_app", {
                "phone_id": phone_id,
                "filename": file.filename,
                "data": b64_data
            }, to=client)

    return "OK", 200

# Run app (Railway requires dynamic port binding)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway sets $PORT
    socketio.run(app, host="0.0.0.0", port=port)
