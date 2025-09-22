from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON data"}), 400

        socketio.emit("new_data", data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@socketio.on("connect")
def on_connect():
    print("LAN client connected")

@socketio.on("disconnect")
def on_disconnect():
    print("LAN client disconnected")

if __name__ == "__main__":
    import eventlet
    import eventlet.wsgi
    # Run with eventlet instead of default Flask server
    socketio.run(app, host="0.0.0.0", port=5000)
