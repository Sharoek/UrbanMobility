from abc import ABC, abstractmethod
from encryption.validators import verify_number_input

class BaseMenu(ABC):
    def __init__(self, username, context):
        self.username = username
        self.context = context
        self.menu_options = {}

    def run(self):
        self.display_header()
        while True:
            self.show_options()
            choice = verify_number_input("Input your choice: ", 0, len(self.menu_options)-1)
            try:
                if choice == 0:
                    return self.context.set_state(None)  # Exit the menu
                state = self.handle_choice(choice)
                
                if state is not None:
                    self.context.set_state(state)
                    print(f"State changed to: {state}")
                    state.run()
                else:
                    return
            except Exception as e:
                print(f"An error occurred: {e}")

    def display_header(self):
        print(f"\nLogged in as: {self.username}\n")


    @abstractmethod
    def show_options(self):
        pass

    @abstractmethod
    def handle_choice(self, choice):
        pass

    def exit_menu(self):
        print("Exiting menu...")
        return False

        

