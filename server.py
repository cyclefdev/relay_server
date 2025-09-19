import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your LAN machine, still on port 5000
LAN_MACHINE_URL = "http://10.0.2.15:5000/store_data"

@app.route("/submit", methods=["POST"])
def submit():
    try:
        # Forward files if present
        files = {"media": request.files["media"]} if "media" in request.files else None
        data = request.form.to_dict()

        resp = requests.post(LAN_MACHINE_URL, data=data, files=files)

        if resp.status_code == 200:
            return jsonify({"message": "Relayed to LAN machine successfully"}), 200
        else:
            return jsonify({"error": "Failed to relay"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Railway provides PORT in env vars, fallback to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
