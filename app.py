import os  
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    
    if not API_KEY:
        return jsonify({"reply": "System Error: API Key missing on server configuration."}), 500
        
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }
    )
    
    data = response.json()
    if "choices" not in data:
        return jsonify({"reply": "Error communicating with AI backend."}), 500
        
    ai_reply = data["choices"][0]["message"]["content"]
    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)