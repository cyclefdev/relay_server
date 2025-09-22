from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Keep track of connected LAN clients
lan_clients = []

@socketio.on('connect')
def handle_connect():
    print("LAN client connected")
    lan_clients.append(request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print("LAN client disconnected")
    if request.sid in lan_clients:
        lan_clients.remove(request.sid)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    files = request.files.to_dict()

    # Forward data to all connected LAN clients
    for sid in lan_clients:
        socketio.emit('data', {'form': data, 'files': list(files.keys())}, room=sid)

    return {'status': 'ok'}

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
