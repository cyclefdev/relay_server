from flask import Flask, request
import os
from datetime import datetime

app = Flask(__name__)

# Base directory where data will be stored
BASE_DIR = "/home/saad/data"  # Make sure this exists on Linux

os.makedirs(BASE_DIR, exist_ok=True)

@app.route("/store_data", methods=["POST"])
def store_data():
    client_ip = request.remote_addr
    print(f"[{datetime.now()}] Received data from {client_ip}")

    # Create directory for this IP
    client_dir = os.path.join(BASE_DIR, client_ip.replace(":", "_"))
    os.makedirs(client_dir, exist_ok=True)

    # Timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(client_dir, f"data_{timestamp}.txt")

    # Store form data
    form_data = request.form.to_dict()
    with open(file_path, "w") as f:
        for key, value in form_data.items():
            f.write(f"{key}: {value}\n")

    print(f"[{datetime.now()}] Data stored in {file_path}")

    # Store any uploaded files
    for filename, file in request.files.items():
        file_save_path = os.path.join(client_dir, f"{timestamp}_{filename}")
        file.save(file_save_path)
        print(f"[{datetime.now()}] File saved: {file_save_path}")

    return "Data received and stored", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

