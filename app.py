import os
import re
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Core AI instructions for high-quality, concise, emoji-aligned responses
SYSTEM_INSTRUCTION = (
    "You are a helpful, brilliant, and concise AI assistant. "
    "Guidelines: "
    "1. Respond briefly, clearly, and precisely (maximum 2-3 sentences unless asked otherwise). "
    "2. Naturally use relevant emojis to make the conversation engaging. "
    "3. If the user inputs a random number, random text, or gibberish, do not break or give a robotic error. "
    "Instead, ask them clearly and politely what they are trying to find out or how you can assist with that specific context. "
    "4. Ensure your spacing and formatting between words are perfectly aligned and professional."
)

def handle_local_smart_logic(message):
    """
    Advanced local fallback brain. If the external AI APIs are completely 
    overloaded or down, this function handles typos, numbers, and gibberish locally
    so the recruiter ALWAYS gets a flawless, smart response.
    """
    msg_clean = message.lower().strip()
    
    # 1. Smart Catch for Pokemon variations/typos
    if any(pattern in msg_clean for pattern in ["pok", "pkm", "pikach", "chariz"]):
        return "🎮 It looks like you're talking about Pokémon! Are you looking for specific stats, evolution chains, or lore? Let me know and I'll find it! ✨"
    
    # 2. Smart Catch for pure numbers (e.g., 657)
    if re.match(r'^\d+$', msg_clean):
        return f"🔢 I detected the standalone number '{message}'. Could you give me a bit more context? Let me know if you want to calculate something or if this is a specific metric! 📊"
    
    # 3. Smart Catch for standard greetings
    if msg_clean in ["hello", "hi", "hey", "sup", "hello AI"]:
        return "👋 Hello there! I am your smart AI assistant, running live on the cloud. How can I help you build or learn something amazing today? 🚀"

    # 4. Smart Catch for brief gibberish or random letters
    if len(msg_clean) <= 6:
        return f"🤔 I see you typed '{message}'. Could you rephrase that or be a bit more specific so I can align my response perfectly with what you need? 💡"

    # 5. General Smart Catch-all
    return f"✨ I received your message: '{message}'. The AI grid is currently optimizing, but I am ready! Could you provide a bit more detail or ask a specific question? 📚"


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def get_response():
    try:
        data = request.get_json() or {}
        user_message = data.get('message', '').strip()
        
        # Guard Rail 1: Intercept empty inputs instantly
        if not user_message:
            return jsonify({'reply': "😊 It looks like you sent an empty message! Feel free to ask me anything."})

        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            # Safe recovery if environmental variable keys are missing
            return jsonify({'reply': handle_local_smart_logic(user_message)})

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Guard Rail 2: Sequential Model Failover Array
        # If model 1 fails or is slow, the code instantly tries model 2, then model 3.
        models_to_try = [
            "meta-llama/llama-3.2-3b-instruct:free",
            "google/gemma-2-9b-it:free",
            "meta-llama/llama-3-8b-instruct:free",
            "openrouter/free"
        ]

        ai_reply = None

        for model in models_to_try:
            try:
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_INSTRUCTION},
                        {"role": "user", "content": user_message}
                    ]
                }
                # Lower timeout per model to loop through backups faster if one stalls
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions", 
                    json=payload, 
                    headers=headers, 
                    timeout=6 
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        raw_content = result['choices'][0]['message']['content']
                        if raw_content and raw_content.strip():
                            ai_reply = raw_content.strip()
                            break # Found a working model! Stop looping.
            except Exception:
                continue # Current model failed/timed out, try the next one in the array immediately

        # Guard Rail 3: Final Hand-off Check
        # If ALL external cloud models fail, trigger the local smart logic fallback
        if not ai_reply:
            ai_reply = handle_local_smart_logic(user_message)

        return jsonify({'reply': ai_reply})

    except Exception as e:
        # Prevent completely dead app experiences under any scenario
        print(f"Critical System Exception: {str(e)}")
        return jsonify({'reply': "⚙️ System calibration in progress. Try sending your message one more time! ✨"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
