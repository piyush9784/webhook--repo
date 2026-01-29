from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# --- DEBUG ENV ---
MONGO_URI = os.getenv("MONGO_URI")
print("MONGO_URI:", MONGO_URI)

if not MONGO_URI:
    raise Exception("MONGO_URI not found")

client = MongoClient(MONGO_URI)
db = client["github_events"]
collection = db["events"]

@app.route("/webhook", methods=["POST"])
def github_webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.get_json()

    print("EVENT TYPE:", event_type)
    print("PAYLOAD:", payload)

    try:
        data = {
            "author": payload.get("author", "unknown"),
            "action": event_type.upper(),
            "from_branch": payload.get("from_branch", ""),
            "to_branch": payload.get("to_branch", ""),
            "timestamp": datetime.utcnow().isoformat()
        }

        result = collection.insert_one(data)
        print("SAVED TO MONGODB:", result.inserted_id)

    except Exception as e:
        print("MONGODB ERROR:", str(e))

    return jsonify({"status": "received"}), 200


if __name__ == "__main__":
    app.run(debug=True)
