from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "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"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    
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
    
    ai_reply = data["choices"][0]["message"]["content"]
    
    return jsonify({
        "reply": ai_reply
    })

if __name__ == "__main__":
    app.run(debug=True)