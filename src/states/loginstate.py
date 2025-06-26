from database.adminrepository import adminRepository
from database.userRepository import UserRepository
from states.appstate import AppState
from encryption.validators import validate_username, validate_password
from states.menustate import MenuState
from log.manager import LogManager

class LoginState(AppState):
    def __init__(self, context):
        super().__init__(context)
        self.context = context
        self.log_manager = LogManager()

    def run(self):
        print("=== Urban Mobility System ===\n")
        for attempt in range(3):
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            if not username or not password:
                print("Username and password cannot be empty.\n")
                continue

            user_repo = UserRepository()

            if username == "super_admin" and password == "Admin_123?":
                self.context.username = username
                self.context.role = "super_admin"
                self.context.user_repo = user_repo
                self.context.set_state(MenuState(self.context))
                self.context.admin_repo = adminRepository()
                return
            
            if not validate_username(username) or not validate_password(password):
                print("Username or password contains invalid characters.\n")
                continue

            
            if user_repo.authenticate_user(username, password):
                self.context.username = username
                self.context.role = user_repo.get_user_role(username)
                self.context.user_repo = user_repo
                self.context.set_state(MenuState(self.context))
                if self.context.role == "system_admin":
                    self.context.admin_repo = adminRepository()
                return

            print(f"Invalid credentials. Attempt {attempt + 1}/3\n")
        print("Too many failed login attempts. Exiting...")
        self.log_manager.log("login", "failed", f"Too many failed login attempts", True)  
        self.context.set_state(None)