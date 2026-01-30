from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["github_events"]
collection = db["events"]

@app.route("/webhook", methods=["POST"])
def github_webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.get_json()

    data = {
        "author": payload.get("author", "unknown"),
        "action": event_type,
        "from_branch": payload.get("from_branch", ""),
        "to_branch": payload.get("to_branch", ""),
        "timestamp": datetime.utcnow().isoformat()
    }

    collection.insert_one(data)
    return jsonify({"status": "received"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    events = list(
        collection.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(10)
    )
    return jsonify(events), 200


if __name__ == "__main__":
    app.run(debug=False)
