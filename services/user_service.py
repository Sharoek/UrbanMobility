from models.user import User
from database.userRepository import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def create_user(self, name: str, email: str) -> int:
        user = User(id=0, name=name, email=email)
        return self.repo.add(user)

    def get_user(self, user_id: int) -> User | None:
        return self.repo.get_by_id(user_id)

    def list_users(self) -> list[User]:
        return self.repo.get_all()
