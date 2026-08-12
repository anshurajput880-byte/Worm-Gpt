from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

WORMGPT_URL = "https://omegatech-api.dixonomega.tech/api/ai/wormgpt"
TIMEOUT = 60

@app.route('/')
def home():
    with open('index.html', 'r') as f:
        return f.read()

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    
    if not message:
        return jsonify({"success": False, "error": "message is required"}), 400
    if len(message) > 4000:
        return jsonify({"success": False, "error": "message too long"}), 400

    try:
        resp = requests.get(
            WORMGPT_URL,
            params={"action": "chat", "message": message},
            timeout=TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0 (WormGPT-Web)"},
        )
        resp.raise_for_status()
        payload = resp.json()

        if not payload.get("success"):
            return jsonify({"success": False, "error": payload.get("error", "API error")}), 502

        return jsonify({
            "success": True,
            "answer": payload.get("content", ""),
            "model": payload.get("model", "unknown"),
            "meta": {
                "source": payload.get("source"),
                "creator": payload.get("creator"),
                "timestamp": payload.get("timestamp"),
            },
        })

    except requests.exceptions.Timeout:
        return jsonify({"success": False, "error": "API timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"Upstream error: {e}"}), 502
    except ValueError:
        return jsonify({"success": False, "error": "Invalid API response"}), 502

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)