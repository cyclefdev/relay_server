from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
import os
import uuid

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
    phone_id = request.form.get('phone_id')
    if not phone_id:
        return "Phone ID is required", 400

    # Forward text and JSON data
    data = {k: v for k, v in request.form.items() if k != "media"}
    data.update(request.json or {})
    for sid in clients:
        socketio.emit("data_from_app", data, to=sid)

    # Handle file uploads
    if "media" in request.files:
        file = request.files["media"]
        filename = f"{phone_id}_{file.filename}"
        for sid in clients:
            socketio.emit("file_from_app", {"filename": filename, "data": file.read()}, to=sid)

    return "Data forwarded", 200

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
