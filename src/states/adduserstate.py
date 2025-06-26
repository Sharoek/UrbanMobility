from models.profile import Profile
from states.appstate import AppState
from encryption.validators import get_valid_input, verify_number_input
from models.user import User
from encryption.validators import validate_username, validate_password, validate_name
from log.manager import LogManager
class addUserState(AppState):

    def __init__(self, context, menu="service_engineer"):
        super().__init__(context)
        self.menu = menu
        self.log_manager = LogManager()
        

    def run(self):
        print("ADDING USER")
        # is it about service Engineer or system admin?
        self.context.set_state(addUserState(self.context))
        self.addUserMenu()


    def addUserMenu(self):
        if self.menu == "service_engineer":
            print("1. Add Service Engineer")
            print("0. Go Back")
        if self.menu == "system_admin":
            print("1. Add System Admin")
            print("0. Go Back")    
        choice = verify_number_input("Enter your choice: ", 0, 1)

        try: 
            if self.menu == "service_engineer":
                if choice == 1:
                    self.inputServiceEngineer()
                if choice == 0:
                    self.context.go_back()
            if self.menu == "system_admin":
                if choice == 1:
                    self.inputSystemAdmin()
                if choice == 0:
                    self.context.go_back()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.context.go_back()


    def inputServiceEngineer(self):
        print("ADDING SERVICE ENGINEER")
        try:
            username = get_valid_input("Enter username: ", validate_username, " Invalid username - 8 to 10 characters,\n Starts with a letter or underscore and Contains only letters,\n digits, underscores, apostrophes, or periods")
            password = get_valid_input("Enter password: ", validate_password, " Invalid password - 12 to 30 characters\n Includes lowercase, uppercase, digit, special character")
            first_name = get_valid_input("Enter first name: ", validate_name, "At least 2 characters, letters only") # needs to be checked if i want that for validation
            last_name = get_valid_input("Enter last name: ", validate_name, "At least 2 characters, letters only")

            new_user = User.create(
                username=username,
                password=password,
                role="service_engineer",
                profile=Profile(first_name=first_name, last_name=last_name)
            )
            self.context.user_repo.save_user_to_db(new_user)
            print("Service Engineer added successfully.")
            self.log_manager.log(self.context.username, "Added Service Engineer", f"Added Service Engineer: {username}")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.log_manager.log(self.context.username, "Failed to add Service Engineer", f"Failed to add Service Engineer: {username}")
        finally:
            self.context.go_back()

    def inputSystemAdmin(self):
        print("ADDING SYSTEM ADMIN")
        try:
            username = get_valid_input("Enter username: ", validate_username, " Invalid username - 8 to 10 characters, \n Starts with a letter or underscore and Contains only letters, \n digits, underscores, apostrophes, or periods")
            password = get_valid_input("Enter password: ", validate_password, " Invalid password - 12 to 30 characters\n Includes lowercase, uppercase, digit, special character")
            first_name = get_valid_input("Enter first name: ", validate_name, "At least 2 characters, letters only") # needs to be checked if i want that for validation
            last_name = get_valid_input("Enter last name: ", validate_name, "At least 2 characters, letters only")

            new_user = User.create(
                username=username,
                password=password,
                role="system_admin",
                profile=Profile(first_name=first_name, last_name=last_name)
            )
            self.context.user_repo.save_user_to_db(new_user)
            self.log_manager.log(self.context.username, "Added System Admin", f"Added System Admin: {username}")
            print("System Admin added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.log_manager.log(self.context.username, "Failed to add System Admin", f"Failed to add System Admin: {username}")
        finally:
            self.context.go_back()
