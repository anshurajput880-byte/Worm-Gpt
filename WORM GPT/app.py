from flask import Flask, request, jsonify, render_template_string
import requests
import os
import json

app = Flask(__name__)

# Your index.html content as a string (or you can keep it as a separate file)
# For now, let's use a simple HTML response
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>WORM GPT</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #0a0a0a;
            color: #00ff41;
        }
        h1 {
            text-align: center;
            font-size: 3em;
            text-shadow: 0 0 20px #00ff41;
        }
        .container {
            background: #111;
            padding: 30px;
            border-radius: 10px;
            border: 1px solid #00ff41;
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.1);
        }
        .status {
            color: #00ff41;
            text-align: center;
            font-size: 1.2em;
        }
        .terminal {
            background: #000;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            color: #00ff41;
            border: 1px solid #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐛 WORM GPT</h1>
        <div class="status">⚡ System Online</div>
        <div class="terminal">
            > Initializing...<br>
            > Loading modules...<br>
            > Ready to serve!
        </div>
        <p style="text-align:center;margin-top:20px;color:#888;">
            Built with Flask | Python 3.13
        </p>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    """Serve the main page"""
    return HTML_TEMPLATE

@app.route('/api/status', methods=['GET'])
def status():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "WORM GPT",
        "version": "1.0.0"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint - handle POST requests"""
    try:
        data = request.get_json()
        
        # If no data sent
        if not data:
            return jsonify({
                "error": "No data provided",
                "message": "Please send JSON data"
            }), 400
        
        # Get user message
        user_message = data.get('message', '')
        
        # Simple response logic (replace with your actual AI logic)
        response_message = f"Received: {user_message}"
        
        return jsonify({
            "response": response_message,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/process', methods=['POST'])
def process():
    """Process data endpoint"""
    try:
        data = request.get_json()
        # Your processing logic here
        return jsonify({
            "processed": True,
            "data": data,
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "status": "error"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "status": "error"
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
