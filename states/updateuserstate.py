from states.appstate import AppState
from encryption.validators import verify_number_input, validate_username, validate_password, validate_name, get_valid_input
from encryption.hashing import hash_password
from models.profile import Profile
from models.user import ServiceEngineer, SystemAdmin


class updateUserState(AppState):
    def __init__(self, context, self_update=False, menu="service_engineer"):
        super().__init__(context)
        self.menu = menu
        self.self_update = self_update

    def run(self):
        print("UPDATING USER")
        self.context.set_state(updateUserState(self.context))
        if self.self_update:
            self.updateSelf()
        self.updateUserMenu()


    def updateSelf(self):
        userID = self.context.admin_repo.getUserID(self.context.username)
        self.update_user_by_id(userID)
        self.context.go_back()



    def updateUserMenu(self):
        while True:
            role_label = "Service Engineer" if self.menu == "service_engineer" else "System Admin"
            print(f"\n1. Update {role_label}")
            print("0. Go Back")

            choice = verify_number_input("Enter your choice: ", 0, 1)
            try:
                if choice == 1:
                    self.inputUser()  
                elif choice == 0:
                    self.context.go_back()
                    break
            except Exception as e:
                print(f"An error occurred: {e}")
                break
            
    def inputUser(self):
        role = self.menu
        pretty_role = "Service Engineer" if role == "service_engineer" else "System Admin"
        print(f"\n-- Update {pretty_role} --")

        users = self.context.admin_repo.get_users_by_role(role)
        if not users:
            print(f"⚠️ No {pretty_role.lower()}s found.")
            self.context.go_back()
            return

        self._print_users(users)
        print("0. Go Back")

        choice = verify_number_input("Select a user to update: ", 0, len(users))
        if choice == 0:
            self.context.go_back()
            return
        user_id = users[choice - 1][0]
        self.update_user_by_id(user_id)

    def update_user_by_id(self, user_id):
        try:
            self.show_attributes_to_update()
            choice = verify_number_input("Select an attribute to update: ", 0, 4)

            if choice == 0:
                self.context.go_back()
                return

            if choice == 1:
                username = get_valid_input(
                    "Enter username: ",
                    validate_username,
                    " Invalid username - 8 to 10 characters,\n Starts with a letter or underscore and Contains only letters,\n digits, underscores, apostrophes, or periods")
                self.context.admin_repo.update_user(user_id, "username", username)

            elif choice == 2:
                password = get_valid_input(
                    "Enter password: ",
                    validate_password,
                    " Invalid password - 12 to 30 characters\n Includes lowercase, uppercase, digit, special character")
                hashed_pw = hash_password(password)
                self.context.admin_repo.update_user(user_id, "password", hashed_pw)

            elif choice == 3:
                first_name = get_valid_input(
                    "Enter first name: ",
                    validate_name,
                    " Invalid first name - 2 to 30 characters,\n Starts with a letter or underscore and Contains only letters,\n digits, underscores, apostrophes, or periods")
                self.context.admin_repo.update_user(user_id, "first_name", first_name)

            elif choice == 4:
                last_name = get_valid_input(
                    "Enter last name: ",
                    validate_name,
                    " Invalid last name - 2 to 30 characters,\n Starts with a letter or underscore and Contains only letters,\n digits, underscores, apostrophes, or periods")
                self.context.admin_repo.update_user(user_id, "last_name", last_name)

            print("✅ User updated successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

        self.context.go_back()

    def show_attributes_to_update(self):
        print("\nAvailable attributes to update:")
        print("1. Username")
        print("2. Password")
        print("3. First Name")
        print("4. Last Name")
        print("0. Go Back")


    def _print_users(self, users):
        count = 1
        if not users:
            print("No users found.")
            return
        print("Available users:")
        for user in users:
            print(f"{count}. ID: {user[0]}, Username: {user[1]}, Name: {user[4]} {user[5]}")
            count+=1
