import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import json

class HashUtils:
    @staticmethod
    def sha256_hash(text: str, iterations: int) -> str:
        hash_hex = text
        for _ in range(iterations):
            hash_hex = hashlib.sha256(hash_hex.encode('utf-8')).hexdigest()
        return hash_hex
    
    @staticmethod
    def pbkdf2_sha256_hash(text: str, iterations: int, salt: bytes) -> str:
        hash_object = hashlib.pbkdf2_hmac('sha256', text.encode('utf-8'), salt, iterations)
        return hash_object.hex()
    
    @staticmethod
    def aes256_encrypt(text: str, key: str) -> str:
        # Ensure the key is 32 bytes (256 bits)
        key = hashlib.sha256(key.encode()).digest()
        
        # Generate random IV (Initialization Vector)
        iv = get_random_bytes(AES.block_size)
        
        # Create cipher object and encrypt the data
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Pad data to be multiple of 16 bytes
        length = 16 - (len(text) % 16)
        text += chr(length) * length
        
        # Encrypt data
        encrypted_data = cipher.encrypt(text.encode())
        
        # Combine IV and encrypted data and encode as base64
        combined = iv + encrypted_data
        return b64encode(combined).decode('utf-8')
    
    @staticmethod
    def aes256_decrypt(combined_text: str, key: str) -> str:
        try:
            # Ensure the key is 32 bytes (256 bits)
            key = hashlib.sha256(key.encode()).digest()
            
            # Decode the combined data from base64
            combined = b64decode(combined_text)
            
            # Split IV and encrypted data
            iv = combined[:AES.block_size]
            encrypted_data = combined[AES.block_size:]
            
            # Create cipher object and decrypt the data
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_data = cipher.decrypt(encrypted_data)
            
            # Unpad the data
            padding_length = decrypted_data[-1]
            decrypted_data = decrypted_data[:-padding_length]
            
            return decrypted_data.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
