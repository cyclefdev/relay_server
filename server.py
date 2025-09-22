import socketio

# Replace this with your actual LAN Linux device URL
LINUX_DEVICE_URL = "http://10.0.2.15:5000/data"

sio = socketio.Client()

@sio.event
def connect():
    print("[+] Connected to relay server")

@sio.event
def disconnect():
    print("[-] Disconnected from relay server")

# Receive data from app and forward to Linux device
@sio.on("send_data")
def handle_data(data):
    import requests
    try:
        # Forward data to Linux device
        requests.post(LINUX_DEVICE_URL, json=data)
        print(f"[>] Forwarded data from device {data.get('device_id')}")
    except Exception as e:
        print(f"[!] Failed to forward data: {e}")

def main():
    # This is the public relay server URL
    RELAY_URL = "https://web-production-57250.up.railway.app/"
    sio.connect(RELAY_URL, transports=["websocket"])
    sio.wait()

if __name__ == "__main__":
    main()
