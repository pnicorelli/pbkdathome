from flask import Blueprint, request, jsonify
from utils.hash_utils import HashUtils
from config import Config

hash_routes = Blueprint('hash_routes', __name__)

@hash_routes.route('/api/encode/sha256', methods=['POST'])
def encode_sha256():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    result = HashUtils.sha256_hash(data['text'], int(data['iterations']))
    return jsonify({'result': result})

@hash_routes.route('/api/encode/pbkdf2-sha256', methods=['POST'])
def encode_pbkdf2_sha256():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    result = HashUtils.pbkdf2_sha256_hash(data['text'], int(data['iterations']), Config.SALT)
    return jsonify({'result': result})

@hash_routes.route('/api/encode/aes256', methods=['POST'])
def encode_aes256():
    data = request.get_json()
    if not data or 'text' not in data or 'key' not in data:
        return jsonify({'error': 'Text and key are required'}), 400
    
    try:
        result = HashUtils.aes256_encrypt(data['text'], data['key'])
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': f'Encryption failed: {str(e)}'}), 500

@hash_routes.route('/api/decode/aes256', methods=['POST'])
def decode_aes256():
    data = request.get_json()
    if not data or 'text' not in data or 'key' not in data:
        return jsonify({'error': 'Encrypted text and key are required'}), 400
    
    try:
        result = HashUtils.aes256_decrypt(data['text'], data['key'])
        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Decryption failed: {str(e)}'}), 500