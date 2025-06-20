from encryption.validators import verify_number_input
from states.appstate import AppState

class deleteUserState(AppState):
    #Delete user service engineer or system_admin
    def __init__(self, context, self_delete=False, menu="service_engineer"):
        super().__init__(context)
        self.menu = menu
        self.self_delete = self_delete
    def run(self):
        print("DELETING USER")
        if self.self_delete:
            try:
                user_id = self.context.admin_repo.getUserID(self.context.username)
                self.context.admin_repo.delete_own_account(user_id)
                print("✅ Deleted your own account successfully.")
                exit()
            except Exception as e:
                print(f"An error occurred: {e}")
            self.context.go_back()
            return
        self._printUsers()
    
    def _printUsers(self):
        role_label = "Service Engineer" if self.menu == "service_engineer" else "System Admin"
        print(f"\n-- Delete {role_label} --")
        index = 1
        try:
            users = self.context.admin_repo.get_users_by_role(self.menu)
            for user in users:
                print(f"{index}. ID: {user[0]}, Username: {user[1]}, Name: {user[4]} {user[5]}")
            print("0. Exit")
            choice = verify_number_input("Select a user to delete: ", 0, len(users))
            if choice == 0:
                self.context.go_back()
                return
            else:
                user_id = users[choice - 1][0]
                self.context.admin_repo.delete_user(user_id, self.context.role)
                print("✅ User deleted successfully.")
                self.context.go_back()
                return
            
        except Exception as e:
            print(f"An error occurred: {e}")
            self.context.go_back()
            return
