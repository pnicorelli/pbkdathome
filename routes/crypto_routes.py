from flask import Blueprint, request, jsonify
from utils.crypto_utils import CryptoUtils
from templates.table_template import generate_address_table

crypto_routes = Blueprint('crypto_routes', __name__)

@crypto_routes.route('/api/encode/bip39', methods=['POST'])
def encode_bip39():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 500
    
    mnemonic = data['text']
    try:
        if not CryptoUtils.validate_mnemonic(mnemonic):
            return jsonify({'error': 'Mnemonic invalid'}), 500
        
        seed_bytes = CryptoUtils.generate_seed(mnemonic)
        return jsonify({'result': seed_bytes.hex()})
    except Exception as e:
        return jsonify({'error': f'Mnemonic format error: {str(e)}'}), 500

@crypto_routes.route('/api/encode/bip44', methods=['POST'])
def generate_bip44_address():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Mnemonic invalid'}), 500
    
    try:
        mnemonic = data['text']
        if not CryptoUtils.validate_mnemonic(mnemonic):
            return jsonify({'error': 'Mnemonic format error'}), 500

        seed_bytes = CryptoUtils.generate_seed(mnemonic)
        error, addresses = CryptoUtils.get_bip44_addresses(
            seed_bytes, 
            data.get('coin', 'BTC'),
            int(data['wallets'])
        )
        
        if error:
            return jsonify({'error': error}), 500
            
        result = generate_address_table(data.get('coin', 'BTC'), addresses)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@crypto_routes.route('/api/encode/bip84', methods=['POST'])
def generate_bip84_address():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Mnemonic invalid'}), 500
    
    try:
        mnemonic = data['text']
        if not CryptoUtils.validate_mnemonic(mnemonic):
            return jsonify({'error': 'Mnemonic format error'}), 500

        seed_bytes = CryptoUtils.generate_seed(mnemonic)
        error, addresses = CryptoUtils.get_bip84_addresses(
            seed_bytes, 
            data.get('coin', 'BTC'),
            int(data['wallets'])
        )
        
        if error:
            return jsonify({'error': error}), 500
            
        result = generate_address_table(data.get('coin', 'BTC'), addresses)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500