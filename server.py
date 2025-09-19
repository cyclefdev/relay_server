import os
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Keep track of connected LAN clients
lan_clients = []

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form.to_dict()
    file_content = None

    if "media" in request.files:
        media_file = request.files["media"]
        file_content = media_file.read()
        filename = media_file.filename or "unknown_file"
        data["media_filename"] = filename

    # Relay to all connected LAN clients
    for client in lan_clients:
        client.emit("data", {"form": data, "media": file_content})

    return jsonify({"message": "Relayed to LAN clients"}), 200

@socketio.on("connect")
def handle_connect():
    lan_clients.append(request.namespace)
    print(f"LAN client connected. Total: {len(lan_clients)}")

@socketio.on("disconnect")
def handle_disconnect():
    if request.namespace in lan_clients:
        lan_clients.remove(request.namespace)
    print(f"LAN client disconnected. Total: {len(lan_clients)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
