from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv(
    MONGO_URI = "mongodb+srv://piyushmehta200_db_user:<db_password>@cluster0.gg2yymv.mongodb.net/?appName=Cluster0"
    
)

client = MongoClient(MONGO_URI)
db = client["github_events"]
collection = db["events"]


@app.route("/webhook", methods=["POST"])
def github_webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    if event_type == "push":
        data = {
            "author": payload.get("author", "unknown"),
            "action": "PUSH",
            "from_branch": payload.get("from_branch", ""),
            "to_branch": payload.get("to_branch", ""),
            "timestamp": datetime.utcnow().isoformat()
        }

        collection.insert_one(data)
        print("Saved to MongoDB:", data)

    return jsonify({"status": "received"}), 200


if __name__ == "__main__":
    app.run(debug=True)
