import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# System prompt forcing brief responses, emoji handling, and smart conversational alignment
SYSTEM_INSTRUCTION = (
    "You are a helpful, brilliant, and concise AI assistant. "
    "Guidelines: "
    "1. Respond briefly, clearly, and precisely (maximum 2-3 sentences unless asked otherwise). "
    "2. Naturally use relevant emojis to make the conversation engaging. "
    "3. If the user inputs a random number, random text, or gibberish, do not break or give a robotic error. "
    "Instead, ask them clearly and politely what they are trying to find out or how you can assist with that specific context. "
    "4. Ensure your spacing and formatting between words are perfectly aligned and professional."
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'response': "⚠️ Internal system error: No payload received."}), 400
            
        user_message = data.get('message', '').strip()
        
        # FIX 1: Catch blank responses instantly BEFORE hitting the API to prevent server queue jamming
        if not user_message:
            return jsonify({'response': "😊 It looks like you sent an empty message! Feel free to ask me anything."})

        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            return jsonify({'response': "🔑 Configuration Error: API key is missing on the server."}), 500

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://render.com", 
            "X-Title": "Tata Steel Chatbot Project"
        }

        payload = {
            # FIX 2: Universal Free Router string guarantees 100% uptime with random/emoji handling
            "model": "openrouter/free",
            "messages": [
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            ai_reply = result['choices'][0]['message']['content'].strip()
            return jsonify({'response': ai_reply})
        else:
            print(f"API Error Code: {response.status_code} - Text: {response.text}")
            return jsonify({'response': "🤖 Oops! The AI core is temporarily busy. Let's try that again. ✨"}), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({'response': "⏳ The request timed out. Please try sending your message again! ✨"})
    except Exception as e:
        print(f"Server Exception: {str(e)}")
        return jsonify({'response': "⚙️ An unexpected error occurred on the server. Let's reboot this chat! ✨"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
