from flask import Flask, send_from_directory, request, jsonify
import hashlib
import os
from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, Bip84, Bip84Coins

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
    
    return jsonify({'result':  hash_hex})

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
    
    return jsonify({'result':  hash_hex})

@app.route('/api/encode/bip39', methods=['POST'])
def encode_bip39():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 500
    mnemonic = data['text']
    try:
        if not Bip39MnemonicValidator().IsValid(mnemonic):
            return jsonify({'error': 'Mnemonic invalid'}), 500
        
        seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
        return jsonify({'result':  seed_bytes.hex()})
    except Exception as e:
        return jsonify({'error': f'Menmonic format error: {str(e)}'}), 500

@app.route('/api/encode/bip44', methods=['POST'])
def generate_bip44_address():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Mnemonic invalid'}), 500
    
    mnemonic = data['text']

    coin = data.get('coin', 'BTC')
    
    try:
        if not Bip39MnemonicValidator().IsValid(mnemonic):
            return jsonify({'error': 'Menmonic format error'}), 500

        seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

        try:
            coin_type = getattr(Bip44Coins, coin.upper())
        except AttributeError:
            return jsonify({'error': f'Coin not supported: {coin}'}), 500

        bip44_obj = Bip44.FromSeed(seed_bytes, coin_type)
        
        wallets = int(data['wallets'])
        result = '<b>' + coin + '</b><br /><table>'
        result = result + '<tr><th>wallet</th><th>address</th><th>PK</th></tr>'
        for i in range(wallets):        
            bip44_addr = bip44_obj.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(i)
            result = result + '<tr>'
            result = result + '<td>' + str(i) + '</td><td><b>' + bip44_addr.PublicKey().ToAddress() + '</b></td>'
            result = result + '<td><b> ' + bip44_addr.PrivateKey().Raw().ToHex() + '</b></td>'
            result = result + '</tr>'
        result = result + '</table>'

        return jsonify({'result':  result})
    except Exception as e:
        return jsonify({'error': f'Error : {str(e)}'}), 500
    

@app.route('/api/encode/bip84', methods=['POST'])
def generate_bip84_address():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Mnemonic invalid'}), 500
    
    mnemonic = data['text']

    coin = data.get('coin', 'BTC')
    
    try:
        if not Bip39MnemonicValidator().IsValid(mnemonic):
            return jsonify({'error': 'Menmonic format error'}), 500

        seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

        try:
            coin_type = getattr(Bip84Coins, coin.upper())
        except AttributeError:
            return jsonify({'error': f'Coin not supported: {coin}'}), 500

        bip44_obj = Bip84.FromSeed(seed_bytes, coin_type)
        
        wallets = int(data['wallets'])
        result = '<b>' + coin + '</b><br /><table>'
        result = result + '<tr><th>wallet</th><th>address</th><th>PK</th></tr>'
        for i in range(wallets):        
            bip44_addr = bip44_obj.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(i)
            result = result + '<tr>'
            result = result + '<td>' + str(i) + '</td><td><b>' + bip44_addr.PublicKey().ToAddress() + '</b></td>'
            result = result + '<td><b> ' + bip44_addr.PrivateKey().Raw().ToHex() + '</b></td>'
            result = result + '</tr>'
        result = result + '</table>'

        return jsonify({'result':  result})
    except Exception as e:
        return jsonify({'error': f'Error : {str(e)}'}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)