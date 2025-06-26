import bcrypt

#hashing will only be used for passwords
# so we can use bcrypt for that purpose
# Bcrypt is a password hashing function designed to be slow and resistant to brute-force attacks.

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
