from flask import Flask, send_from_directory, request, jsonify
import hashlib
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/encode/sha256', methods=['POST'])
def encode_sha256():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    hash_hex = data['text']
    iterations = int(data['iterations'])

    for i in range(iterations):
        hash_hex = hashlib.sha256(hash_hex.encode('utf-8'))
        hash_hex = hash_hex.hexdigest()
    
    return jsonify({'hash': hash_hex})

@app.route('/api/encode/pbkdf2-sha256', methods=['POST'])
def encode_pbkdf2_sha256():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    iterations = int(data['iterations'])
    salt = os.environ.get('SALT', 'salt_missing').encode('utf-8') 
    hash_object = hashlib.pbkdf2_hmac('sha256', text.encode('utf-8'), salt, iterations)
    hash_hex = hash_object.hex()
    
    return jsonify({'hash': hash_hex})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)