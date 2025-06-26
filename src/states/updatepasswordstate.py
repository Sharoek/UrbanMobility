from .appstate import AppState
from encryption.validators import validate_password
from log.manager import LogManager

class UpdatePasswordState(AppState):
    def __init__(self, context):
        super().__init__(context)
        self.log_manager = LogManager()

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
        try:
            while True:
                new_password = input("Enter new password: ").strip()
                confirm_password = input("Confirm new password: ").strip()
                old_password = input("Enter old password: ").strip()

                if validate_password(new_password):
                    break
                elif new_password != confirm_password:
                    print("Passwords do not match. Please try again.")
                else:
                    print("New password is invalid. It needs to be at least 12 characters long, contain uppercase and lowercase letters, numbers, and special characters.")    

            if self.context.user_repo.update_own_password(username, old_password, new_password):
                print(f"Password for user '{username}' has been updated successfully.")
                self.log_manager.log(username, "Password Update", f"Password updated successfully for user {username}")
            else:
                print(f"Failed to update password for user '{username}'.")
                self.log_manager.log(username, "Password Update", f"Failed to update password for user {username}")
        except Exception as e:
            print(f"An error occurred while updating the password: {e}")
            self.log_manager.log(username, "Password Update", f"Failed to update password for user {username}: {e}", True)
            

        self.context.go_back()