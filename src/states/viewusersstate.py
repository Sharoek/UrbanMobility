from states.appstate import AppState
from encryption.validators import verify_number_input
class viewUsersState(AppState):
    def run(self):
        print("VIEWING USERS")
        self.context.set_state(viewUsersState(self.context))
        try: 
            self.context.admin_repo.view_users()
            print("Press 0 to go back")
            choice = verify_number_input("Enter your choice: ", 0, 0)
            if choice == 0:
                self.context.go_back()
        except Exception as e:
            print(f"An error occurred: {e}")    
