import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_response():
    user_input = request.json.get('message')
    print(f"[User] {user_input}")  # Debug print

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  
        chat = model.start_chat(history=[])
        response_raw = chat.send_message(user_input)
        response = response_raw.text
        print(f"[Gemini] {response}")  
        return jsonify({'response': response})
    except Exception as e:
        print(f"[Error] {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    