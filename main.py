from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

SERIAL_DB = "serial_keys.json"

# Create a file if not exists
if not os.path.exists(SERIAL_DB):
    with open(SERIAL_DB, "w") as f:
        json.dump({"valid_keys": {}, "activated_keys": []}, f)

def load_keys():
    with open(SERIAL_DB, "r") as f:
        return json.load(f)

def save_keys(data):
    with open(SERIAL_DB, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/verify", methods=["POST"])
def verify_key():
    data = request.json
    serial_key = data.get("serial_key")

    db = load_keys()
    
    if serial_key in db["valid_keys"] and serial_key not in db["activated_keys"]:
        db["activated_keys"].append(serial_key)  # Mark as used
        save_keys(db)
        return jsonify({"status": "success", "message": "Key activated!"})
    elif serial_key in db["activated_keys"]:
        return jsonify({"status": "error", "message": "Key already activated!"})
    else:
        return jsonify({"status": "error", "message": "Invalid key!"})

@app.route("/add_key", methods=["POST"])
def add_key():
    data = request.json
    new_key = data.get("serial_key")

    db = load_keys()
    
    if new_key in db["valid_keys"]:
        return jsonify({"status": "error", "message": "Key already exists!"})

    db["valid_keys"][new_key] = True  # Add key
    save_keys(db)
    return jsonify({"status": "success", "message": "Key added!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Use port 10000 for Render
