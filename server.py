import os
from flask import Flask, request, jsonify
import requests
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# LAN machine (optional)
LAN_MACHINE_URL = "http://10.0.2.15:5000/store_data"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form.to_dict()
    files = {"media": request.files["media"]} if "media" in request.files else None

    try:
        resp = requests.post(LAN_MACHINE_URL, data=data, files=files, timeout=2)
        if resp.status_code == 200:
            return jsonify({"message": "Relayed to LAN machine successfully"}), 200
        else:
            return jsonify({"warning": "LAN relay failed", "status": resp.status_code}), 200
    except requests.exceptions.RequestException:
        return jsonify({"message": "Data received. LAN machine offline."}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
