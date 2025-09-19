import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# LAN machine URL (optional, may not always be running)
LAN_MACHINE_URL = "http://10.0.2.15:5000/store_data"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form.to_dict()
    files = {"media": request.files["media"]} if "media" in request.files else None

    # Try relaying to LAN machine, but don't crash if unreachable
    try:
        resp = requests.post(LAN_MACHINE_URL, data=data, files=files, timeout=2)
        if resp.status_code == 200:
            return jsonify({"message": "Relayed to LAN machine successfully"}), 200
        else:
            return jsonify({
                "warning": "Server up, but LAN relay failed",
                "relay_status": resp.status_code
            }), 200
    except requests.exceptions.RequestException:
        # LAN machine is down or unreachable
        return jsonify({
            "message": "Data received. LAN machine is offline, will not relay now."
        }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway sets PORT, fallback to 5000 locally
    app.run(host="0.0.0.0", port=port)
