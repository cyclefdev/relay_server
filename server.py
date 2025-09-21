from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import base64

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/submit", methods=["POST"])
def submit():
    phone_id = request.form.get("phone_id")
    form_data = dict(request.form)
    form_data.pop("media", None)

    payload = {"form": form_data}

    if "media" in request.files:
        media_file = request.files["media"]
        payload["media"] = base64.b64encode(media_file.read()).decode("utf-8")
        payload["media_filename"] = media_file.filename

    # Emit to connected Linux client
    socketio.emit("data", payload)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
