import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from chatbot import Chatbot

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for frontend

bot = Chatbot('intents.json')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({'response': "I didn't catch that. Can you say it again?"})
    
    response = bot.get_response(user_input)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
