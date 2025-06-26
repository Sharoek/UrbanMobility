from cryptography.hazmat.primitives.ciphers.aead import AESSIV
import base64
from encryption.key_management import load_key

# AES-SIV needs a 64-byte key for AES-256-SIV
# AES-SIV is a deterministic authenticated encryption mode that provides both confidentiality and integrity.
# It is suitable for encrypting data that needs to be both secure and verifiable.  
# Deterministic means that the same plaintext will always produce the same ciphertext, which is useful in this use case.
key = load_key()
siv = AESSIV(key)

def encrypt_data(value: str) -> str:
    if isinstance(value, (int, float)):
        value = str(value)
    ciphertext = siv.encrypt(value.encode(), [])
    return base64.b64encode(ciphertext).decode()

def decrypt_data(encrypted_value: str) -> str:
    ciphertext = base64.b64decode(encrypted_value)
    plaintext = siv.decrypt(ciphertext, [])
    return plaintext.decode()