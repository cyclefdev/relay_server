from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

# Directory to store all phone data
LOCAL_STORAGE_DIR = "/home/saad/phone_data"
os.makedirs(LOCAL_STORAGE_DIR, exist_ok=True)

@app.route("/store_data", methods=["POST"])
def store_data():
    phone_id = request.form.get("phone_id")
    if not phone_id:
        return jsonify({"error": "phone_id required"}), 400

    # Create a folder for this phone_id
    phone_dir = os.path.join(LOCAL_STORAGE_DIR, phone_id)
    os.makedirs(phone_dir, exist_ok=True)

    # Store form data except media
    form_data = {k: v for k, v in request.form.items() if k != "media"}
    form_path = os.path.join(phone_dir, "form.json")
    with open(form_path, "w", encoding="utf-8") as f:
        json.dump(form_data, f, indent=2, ensure_ascii=False)

    # Store uploaded media
    if "media" in request.files:
        media_file = request.files["media"]
        filename = media_file.filename or "unknown_file"
        media_file.save(os.path.join(phone_dir, filename))

    return jsonify({"message": "Stored on Linux machine successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

