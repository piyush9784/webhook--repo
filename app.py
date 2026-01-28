from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def github_webhook():
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json

    print("Received GitHub Event:", event_type)
    print("Payload:", payload)

    return jsonify({"status": "received"}), 200


if __name__ == "__main__":
    app.run(debug=True)
