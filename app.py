import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

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

@app.route('/chat', methods=['POST'])
def get_response():
    try:
        data = request.get_json() or {}
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'reply': "😊 It looks like you sent an empty message! Feel free to ask me anything."})

        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            return jsonify({'reply': "🔑 Configuration Error: API key missing from Render Environment."}), 500

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # SWAPPED: Using the ultra-stable LLaMA 3.2 3B Free model to eliminate saturation errors!
        payload = {
            "model": "meta-llama/llama-3.2-3b-instruct:free",
            "messages": [
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", 
            json=payload, 
            headers=headers, 
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                ai_reply = result['choices'][0]['message']['content'].strip()
                return jsonify({'reply': ai_reply})
            else:
                return jsonify({'reply': "⚠️ Received empty structure from AI model backend."})
        else:
            print(f"OpenRouter Error Status: {response.status_code} - Log: {response.text}")
            return jsonify({'reply': "🤖 System load is highly saturated right now. Let's retry that prompt! ✨"}), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({'reply': "⏳ Connection timed out. Let's try sending that once more! ✨"})
    except Exception as e:
        print(f"Backend Exception Triggered: {str(e)}")
        return jsonify({'reply': f"⚙️ Server pipeline exception: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
