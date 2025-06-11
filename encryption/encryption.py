from cryptography.fernet import Fernet
import os

KEY_FILE = "fernet.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

cipher = Fernet(load_key())

def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    return cipher.decrypt(encrypted_data.encode()).decode()
