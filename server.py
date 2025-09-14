from flask import Flask, request
from flask_socketio import SocketIO, emit
import base64

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

linux_clients = []

@socketio.on("connect")
def on_connect():
    linux_clients.append(request.sid)
    print(f"Linux connected: {request.sid}")

@socketio.on("disconnect")
def on_disconnect():
    linux_clients.remove(request.sid)
    print(f"Linux disconnected: {request.sid}")

@app.route("/submit", methods=["POST"])
def submit():
    phone_id = request.form.get("phone_id")
    if not phone_id:
        return "Missing phone_id", 400

    data = {k: v for k, v in request.form.items() if k != "media"}

    # Forward metadata
    for client in linux_clients:
        socketio.emit("data_from_app", {"phone_id": phone_id, "data": data}, to=client)

    # Forward file if exists
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

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)

