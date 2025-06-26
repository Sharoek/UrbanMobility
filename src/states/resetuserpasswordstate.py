from states.appstate import AppState
from encryption.validators import validate_password, verify_number_input


class resetUserPasswordState(AppState):
    def __init__(self, context, user="service_engineer"):
        super().__init__(context)
        self.user = user

    def run(self):
        role = self.context.role
        pretty_role = "Service Engineer" if role == "system_admin" else "User"

        print(f"\n-- Reset {pretty_role} Password --")

        users = self.context.admin_repo.get_users_by_role(self.user)

        if not users:
            print("⚠️ No users found.")
            return self.context.go_back()

        # Print users
        for idx, user in enumerate(users, start=1):
            print(f"{idx}. ID: {user[0]}, Username: {user[1]}")
        print("0. Go Back")

        choice = verify_number_input("Select a user to reset password: ", 0, len(users))
        if choice == 0:
            return self.context.go_back()

        user_id = users[choice - 1][0]

        if validate_password("StrongPass!123"):
            new_password = "StrongPass!123"

        # Update password
        try:
            self.context.admin_repo.reset_password(user_id, new_password)
            print(f"✅ Password updated successfully for user ID {user_id}.")
        except Exception as e:
            print(f"[✖] Failed to update password: {e}")

        self.context.go_back()
