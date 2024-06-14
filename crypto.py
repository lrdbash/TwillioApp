from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

KEY_FILE = 'aes_key.bin'

def generate_key():
    key = get_random_bytes(32)  # AES-256
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    with open(KEY_FILE, 'rb') as key_file:
        key = key_file.read()
    return key

def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return base64.b64encode(nonce + tag + ciphertext).decode('utf-8')

def decrypt_message(key, encrypted_message):
    encrypted_message_bytes = base64.b64decode(encrypted_message)
    nonce = encrypted_message_bytes[:16]
    tag = encrypted_message_bytes[16:32]
    ciphertext = encrypted_message_bytes[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_message = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_message.decode('utf-8')
