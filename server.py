import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

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
        # LAN machine offline, server still alive
        return jsonify({"message": "Data received. LAN machine offline."}), 200

if __name__ == "__main__":
    # Railway dynamically sets this
    port = int(os.environ.get("PORT", 5000))  # fallback 5000 for local dev
    app.run(host="0.0.0.0", port=port)
