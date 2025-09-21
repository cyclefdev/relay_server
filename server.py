import os
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

# Create Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecret"  # change if you want

# Initialize SocketIO with eventlet
socketio = SocketIO(app, cors_allowed_origins="*")  

# Simple HTTP route (optional, for testing)
@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "Server is running!"})

# Example WebSocket event
@socketio.on("connect")
def handle_connect():
    print("Client connected")
    emit("message", {"data": "Welcome! Connected to server."})

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

@socketio.on("send_data")
def handle_send_data(data):
    print("Received data:", data)
    emit("data_received", {"status": "success", "data": data}, broadcast=True)

if __name__ == "__main__":
    # Railway provides the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
