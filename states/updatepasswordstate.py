from .appstate import AppState
from encryption.validators import validate_password
class UpdatePasswordState(AppState):
    def run(self):
        # if self.context.role != "service_engineer":
        #     print("Access denied. This function is only available to service engineers.")
        #     self.context.set_state(None)
        #     return
        print("=== Update Password ===\n")
        username = self.context.username
        if not username:
            print("No user is currently logged in.")
            return

        while True:
            new_password = input("Enter new password: ").strip()
            confirm_password = input("Confirm new password: ").strip()
            old_password = input("Enter old password: ").strip()

            if not validate_password(new_password):
                print("New password is invalid. It needs to be at least 12 characters long, contain uppercase and lowercase letters, numbers, and special characters.")
            else:
                break     

        if new_password != confirm_password:
            print("Passwords do not match. Please try again.")
            return

        if self.context.user_repo.update_own_password(username, old_password, new_password):
            print(f"Password for user '{username}' has been updated successfully.")
        else:
            print(f"Failed to update password for user '{username}'.")

        self.context.go_back()