import base64
import json
import os
import uuid
from io import BytesIO
from flask import Flask, request, jsonify, render_template, redirect, url_for

try:
    import qrcode
except ImportError:
    qrcode = None

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
app = Flask(__name__)


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(records):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/records", methods=["GET"])
def list_records():
    return jsonify(load_data())


@app.route("/api/records", methods=["POST"])
def create_record():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400
    record = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": payload.get("email", ""),
        "phone": payload.get("phone", ""),
    }
    records = load_data()
    records.append(record)
    save_data(records)
    return jsonify(record), 201


@app.route("/api/records/<record_id>", methods=["GET"])
def read_record(record_id):
    record = next((r for r in load_data() if r["id"] == record_id), None)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(record)


@app.route("/api/records/<record_id>", methods=["PUT"])
def update_record(record_id):
    payload = request.get_json(silent=True) or {}
    records = load_data()
    record = next((r for r in records if r["id"] == record_id), None)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    record["name"] = payload.get("name", record["name"])
    record["email"] = payload.get("email", record["email"])
    record["phone"] = payload.get("phone", record["phone"])
    save_data(records)
    return jsonify(record)


@app.route("/api/records/<record_id>", methods=["DELETE"])
def delete_record(record_id):
    records = load_data()
    filtered = [r for r in records if r["id"] != record_id]
    if len(filtered) == len(records):
        return jsonify({"error": "Record not found"}), 404
    save_data(filtered)
    return "", 204


@app.route("/api/qrcode", methods=["POST"])
def generate_qrcode():
    if qrcode is None:
        return jsonify({"error": "QR code generator is unavailable. Install qrcode with pip."}), 500
    payload = request.get_json(silent=True) or {}
    data = (payload.get("text") or "").strip()
    if not data:
        return jsonify({"error": "Text is required"}), 400

    img = qrcode.make(data)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode("ascii")
    return jsonify({"data_uri": f"data:image/png;base64,{encoded}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
