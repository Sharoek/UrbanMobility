from database.connection import get_connection
from models.user import User
from database.queries import INSERT_USER, GET_USER_BY_ID, GET_ALL_USERS
from encryption.encryption import encrypt_data
from encryption.hashing import verify_password, hash_password

class UserRepository:
    def __init__(self):
        pass    

    def save_user_to_db(self, user: User):
        with get_connection() as conn:
            encrypted_first = encrypt_data(user.profile.first_name)
            encrypted_last = encrypt_data(user.profile.last_name)
            encrypt_username = encrypt_data(user.username)
            try:
                conn.execute(INSERT_USER, (encrypt_username, user.password_hash, user.role, encrypted_first, encrypted_last, user.profile.registration_date))
                conn.commit()
                print(f"[✔] User '{user.username}' added as {user.role}.")
            except Exception as e:
                print(f"[✖] Error saving user: {e}")
                return False
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user by checking username and password."""
        # hash password is not the same as in the database so get password hash from the database and decrypt it
        username = encrypt_data(username)
        print(f"[i] Authenticating user: {username}")
        with get_connection() as conn:
            cursor = conn.execute("SELECT password FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if verify_password(password, row["password"]):
                print("[✔] Authentication successful.")
                return True
        return False
    
    def get_user_role(self, username: str) -> str:
        """Get the role of a user by username."""
        username = encrypt_data(username)
        with get_connection() as conn:
            cursor = conn.execute("SELECT role FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return row["role"]
        return "unknown"
    
    def update_password(self, username: str, new_password: str) -> bool:
        """Update the password for a user."""
        username = encrypt_data(username)
        new_password_hash = hash_password(new_password)
        with get_connection() as conn:
            try:
                conn.execute("UPDATE users SET password = ? WHERE username = ?", (new_password_hash, username))
                conn.commit()
                print(f"[✔] Password for user '{username}' has been updated successfully.")
                return True
            except Exception as e:
                print(f"[✖] Error updating password: {e}")
                return False
    #redundant?
    def update_own_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Update the password for the currently logged-in user."""
        if not self.authenticate_user(username, old_password):
            print("[✖] Old password is incorrect.")
            return False
        return self.update_password(username, new_password)
    
