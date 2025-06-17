import os

KEY_FILE = "siv.key"

def generate_key():
    key = os.urandom(64)  # AES-SIV needs 64 bytes for 256-bit key
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()