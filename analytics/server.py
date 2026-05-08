from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_FILE = 'interactions.json'

MOCK_RESPONSES = [
    "That's an interesting question! Here's what I think...",
    "I understand your query. Let me provide some insights.",
    "Great question! The answer depends on several factors.",
    "Based on my analysis, I would suggest the following approach.",
    "This is a complex topic. Let me break it down for you.",
]

def load_interactions():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_interactions(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    model = data.get('model', 'mock-gpt-4')

    # Mock AI response
    ai_response = random.choice(MOCK_RESPONSES)
    tokens_used = random.randint(50, 500)
    response_time = round(random.uniform(0.3, 2.5), 2)

    interaction = {
        'id': len(load_interactions()) + 1,
        'timestamp': datetime.utcnow().isoformat(),
        'user_message': user_message,
        'ai_response': ai_response,
        'model': model,
        'tokens_used': tokens_used,
        'response_time_sec': response_time
    }

    interactions = load_interactions()
    interactions.append(interaction)
    save_interactions(interactions)

    return jsonify({
        'response': ai_response,
        'tokens_used': tokens_used,
        'response_time': response_time,
        'model': model
    })

@app.route('/api/analytics', methods=['GET'])
def analytics():
    interactions = load_interactions()
    if not interactions:
        return jsonify({'total': 0, 'interactions': [], 'stats': {}})

    total_tokens = sum(i['tokens_used'] for i in interactions)
    avg_response_time = round(
        sum(i['response_time_sec'] for i in interactions) / len(interactions), 2
    )
    models_used = {}
    for i in interactions:
        m = i['model']
        models_used[m] = models_used.get(m, 0) + 1

    # Messages per day
    per_day = {}
    for i in interactions:
        day = i['timestamp'][:10]
        per_day[day] = per_day.get(day, 0) + 1

    return jsonify({
        'total': len(interactions),
        'interactions': interactions[-20:],
        'stats': {
            'total_tokens': total_tokens,
            'avg_tokens_per_message': round(total_tokens / len(interactions), 1),
            'avg_response_time_sec': avg_response_time,
            'models_used': models_used,
            'messages_per_day': per_day
        }
    })

@app.route('/api/interactions', methods=['DELETE'])
def clear():
    save_interactions([])
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
