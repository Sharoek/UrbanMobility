from database.connection import get_connection
from models.user import User
from database.queries import INSERT_USER, GET_USER_BY_ID, GET_ALL_USERS
from encryption.encryption import encrypt_data
class UserRepository:
    def add(self, user: User) -> int:
        with get_connection() as conn:
            cursor = conn.execute(INSERT_USER, (user.name, user.email))
            conn.commit()
            return cursor.lastrowid

    def get_by_id(self, user_id: int) -> User | None:
        with get_connection() as conn:
            row = conn.execute(GET_USER_BY_ID, (user_id,)).fetchone()
            if row:
                return User(id=row["id"], name=row["name"], email=row["email"])
            return None

    def get_all(self) -> list[User]:
        with get_connection() as conn:
            rows = conn.execute(GET_ALL_USERS).fetchall()
            return [User(id=row["id"], name=row["name"], email=row["email"]) for row in rows]

    def save_user_to_db(self, user: User) -> None:
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