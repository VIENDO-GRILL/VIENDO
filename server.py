import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')

TELEGRAM_BOT_TOKEN = '8604835546:AAGV-7jAFk7_EfUGR-_QQyUUF-z4lSEt3Fw'
TELEGRAM_CHAT_ID   = '5794299315'

@app.route('/send-telegram', methods=['POST'])
def send_telegram():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'ok': False, 'error': 'no text'}), 400
    try:
        r = requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
            json={'chat_id': TELEGRAM_CHAT_ID, 'text': text, 'parse_mode': 'HTML'},
            timeout=10
        )
        return jsonify(r.json())
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join('.', path)):
        return send_from_directory('.', path)
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
