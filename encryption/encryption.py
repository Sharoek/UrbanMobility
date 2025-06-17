from cryptography.hazmat.primitives.ciphers.aead import AESSIV
import base64
from encryption.key_management import load_key

# AES-SIV needs a 64-byte key for AES-256-SIV
key = load_key()
siv = AESSIV(key)

def encrypt_data(value: str) -> str:
    ciphertext = siv.encrypt(value.encode(), [])
    return base64.b64encode(ciphertext).decode()

def decrypt_data(encrypted_value: str) -> str:
    ciphertext = base64.b64decode(encrypted_value)
    plaintext = siv.decrypt(ciphertext, [])
    return plaintext.decode()