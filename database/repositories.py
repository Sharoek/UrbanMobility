from database.connection import get_connection
from models.user import User
from database.queries import INSERT_USER, GET_USER_BY_ID, GET_ALL_USERS

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
